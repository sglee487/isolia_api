import random
import json
import os
import threading
import asyncio

from fastapi import APIRouter, WebSocket
from gunicorn.workers.base import Worker
import shortuuid

# from socketio import AsyncServer
# from ..main import socket_manager as sm
from starlette.websockets import WebSocketDisconnect
import redis

from utils.mine import generate_nickname, generate_color

from decouple import config

router = APIRouter()
r = redis.Redis(
    host=str(config('REDIS_HOST')),
    port=int(config('REDIS_PORT')),
    db=int(config('MINE_REDIS_DB')),
    charset="utf-8",
    decode_responses=True,
)
pubsub = r.pubsub()
pubsub.subscribe('mine')
active_connections_key = 'active_connections'
profiles_key = 'profiles'
history_key = 'history'
size_key = 'size'
bomb_key = 'bomb'
bomb_coords_key = 'bomb_coords'

r.set(size_key, 12)
r.set(bomb_key, 20)


def get_redis_size():
    size = int(r.get(size_key) or 0)
    return size


def get_redis_bomb():
    bomb = int(r.get(bomb_key) or 0)
    return bomb


def get_redis_bomb_coords():
    bomb_coords = r.get(bomb_coords_key) or '[]'
    return bomb_coords


def get_history():
    history = []
    for history_str in r.lrange(history_key, 0, -1):
        history.append(json.loads(history_str))
    return history


def game_reset():
    r.delete(history_key)
    bomb_coords = []

    size = int(r.get(size_key) or 0)
    bombs = int(r.get(bomb_key) or 0)

    for _ in range(bombs):
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        bomb_coords.append((row, col))

    r.set(bomb_coords_key, json.dumps(bomb_coords))


game_reset()


class ConnectionManager:
    def __init__(self):
        listener = threading.Thread(target=self.between_worker)
        listener.start()
        self.websockets: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, sid: str):
        profile = {
            "sid": sid,
            "name": generate_nickname(),
            "color": generate_color(),
        }
        self.websockets[sid] = websocket
        r.set(sid, json.dumps(profile))
        r.lpush(profiles_key, json.dumps(profile))
        await websocket.send_json({"type": "profile", **profile})

    async def disconnect(self, sid: str):
        if sid in self.websockets:
            del self.websockets[sid]
        await self.mine_players()

    async def mine_players(self):
        print(os.getpid(), 'mine_players')
        players = []
        for profile_str in r.lrange(profiles_key, 0, -1):
            profile = json.loads(profile_str)
            players.append({"sid": profile['sid'], "name": profile["name"], "color": profile["color"]})

        for ws in self.websockets.values():
            await ws.send_json({"type": "players", "players": players})

    async def mine_start(self, websocket: WebSocket):
        await websocket.send_json(
            {
                "type": "start",
                "size": get_redis_size(),
                "bomb_coords": get_redis_bomb_coords(),
                "history": get_history(),
            }
        )

    async def mine_action(self, sid: str, data: dict):
        profile_str = r.get(sid)
        if not profile_str:
            return

        profile = json.loads(profile_str)
        name = profile['name']
        color = profile['color']
        response_data = {**data, "name": name, "color": color}
        r.lpush(history_key, json.dumps(response_data))
        r.publish('mine', json.dumps({"type": "action", **response_data}))

    async def mine_reset(self):
        global size

        response_data = {
            "type": "restart",
            "size": get_redis_size(),
            "bomb_coords": get_redis_bomb_coords(),
            "history": [],
        }

        for profile_str in r.lrange(profiles_key, 0, -1):
            profile = json.loads(profile_str)
            if profile['sid'] in self.websockets:
                await self.websockets[profile['sid']].send_json(response_data)

    async def broadcast(self, data: dict):
        if data['type'] == 'action':
            profile = json.loads(r.get(data['sid']) or '')
            response_data = {
                'type': 'action',
                'action': data['action'],
                'x': data['x'],
                'y': data['y'],
                'name': profile['name'],
                'color': profile['color'],
                "history": get_history(),
            }

            for profile_str in r.lrange(profiles_key, 0, -1):
                profile = json.loads(profile_str)
                if profile['sid'] in self.websockets:
                    await self.websockets[profile['sid']].send_json(response_data)
        elif data['type'] == 'disconnect':
            await self.disconnect(data['sid'])

    async def worker(self):
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                if data['type'] == 'reset':
                    await self.mine_reset()
                elif data['type'] == 'players':
                    await self.mine_players()
                elif data['type'] == 'action':
                    await self.broadcast(data)
                elif data['type'] == 'disconnect':
                    await self.disconnect(data['sid'])
        time.sleep(0.001)

    def between_worker(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.worker())
        loop.close()


connection_manager = ConnectionManager()


import time


@router.websocket("/ws/mine_connect")
async def connect(websocket: WebSocket):
    await websocket.accept()

    sid = shortuuid.uuid()
    try:
        await connection_manager.connect(websocket, sid)

        while True:
            data = await websocket.receive_json()
            if data['type'] == "start":
                await connection_manager.mine_start(websocket)
            elif data['type'] == "players":
                r.publish(
                    'mine',
                    json.dumps({"type": "players"}),
                )
            elif data['type'] == "action":
                sid = data['sid']
                await connection_manager.mine_action(sid, data)
            elif data['type'] == 'reset':
                game_reset()
                r.publish(
                    'mine',
                    json.dumps(
                        {
                            "type": "reset",
                            "size": get_redis_size(),
                            "bomb_coords": get_redis_bomb_coords(),
                            "history": [],
                        }
                    ),
                )

    except WebSocketDisconnect:
        r.delete(sid)
        list_values = r.lrange(profiles_key, 0, -1)
        for value in list_values:
            if json.loads(value)['sid'] == sid:
                r.lrem(profiles_key, 0, value)
        r.publish('mine', json.dumps({"type": "disconnect", "sid": sid}))
        await connection_manager.broadcast({"type": "disconnect", "sid": sid})

    return
