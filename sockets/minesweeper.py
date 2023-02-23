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

router = APIRouter()
redis_url = 'redis://127.0.0.1:6379/0'
r = redis.Redis(host='127.0.0.1', port=6379, db=0, charset="utf-8", decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe('mine')
active_connections_key = 'active_connections'
profiles_key = 'profiles'
history_key = 'history'
size_key = 'size'
bomb_key = 'bomb'
bomb_coords_key = 'bomb_coords'

# size = 12
r.set(size_key, 12)
# bombs = 4
r.set(bomb_key, 4)
# bomb_coords = []
# r.set(bomb_coords_key, json.dumps([]))


def get_redis_size():
    size = int(r.get(size_key) or 0)
    return size


def get_redis_bomb():
    bomb = int(r.get(bomb_key) or 0)
    return bomb


def get_redis_bomb_coords():
    bomb_coords = r.get(bomb_coords_key) or '[]'
    return bomb_coords


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
        # players = []
        # for sid in r.scan_iter():
        #     profile_str = r.get(sid)
        #     if profile_str:
        #         profile = json.loads(profile_str)
        #         if 'mine_players_ws' in profile:
        #             players.append({"name": profile["name"], "color": profile["color"]})
        # for sid in r.scan_iter():
        #     profile_str = r.get(sid)
        #     if profile_str:
        #         profile = json.loads(profile_str)
        #         if 'mine_players_ws' in profile:

        # r.delete(sid)
        # print(json.loads(profile))
        #     profile = json.loads(r.get(sid))
        #     if 'mine_players_ws' in profile:
        #         players.append({"name": profile["name"], "color": profile["color"]})
        # for profile in self.profiles.values():
        #     if 'mine_players_ws' in profile:
        #         await profile['mine_players_ws'].send_json(players)

    async def mine_players(self):
        # r.set(sid, 'mine_players_ws', websocket)
        players = []
        for profile_str in r.lrange(profiles_key, 0, -1):
            profile = json.loads(profile_str)
            players.append({"name": profile["name"], "color": profile["color"]})

        # for profile in self.profiles.values():
        #     if 'mine_players_ws' in profile:
        #         players.append({"name": profile["name"], "color": profile["color"]})
        # for profile in self.profiles.values():
        #     if 'mine_players_ws' in profile:
        #         await profile['mine_players_ws'].send_json(players)
        for ws in self.websockets.values():
            await ws.send_json({"type": "players", "players": players})

    async def mine_start(self, websocket: WebSocket):
        await websocket.send_json(
            {
                "type": "start",
                "size": get_redis_size(),
                "bomb_coords": get_redis_bomb_coords(),
                "history": r.lrange(history_key, 0, -1),
            }
        )

    async def mine_action(self, websocket: WebSocket, sid: str, data: dict):
        # print(data)
        print(sid)
        print(r.get(sid))
        profile_str = r.get(sid)
        print(type(profile_str))
        if not profile_str:
            return

        profile = json.loads(profile_str)
        name = profile['name']
        color = profile['color']
        response_data = {**data, "name": name, "color": color}
        r.lpush(history_key, json.dumps(response_data))
        # self.broadcast("type": "action", **response_data)
        r.publish('mine', json.dumps({"type": "action", **response_data}))
        # await websocket.send_json({"type": "action", **data, "history": [response_data]})

        # self.profiles[sid]['mine_action_ws'] = websocket
        # try:
        #     while True:
        #         data = await websocket.receive_json()
        #         response_data = {
        #             **data,
        #             "name": self.profiles[sid]["name"],
        #             "color": self.profiles[sid]["color"],
        #         }
        #         history.append(response_data)
        #         for profile in self.profiles.values():
        #             if 'mine_action_ws' in profile:
        #                 await profile['mine_action_ws'].send_json({**response_data, "history": history})

    #     except WebSocketDisconnect:
    #         return

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

        # for profile in self.profiles.values():
        #     if 'mine_start_ws' in profile:
        #         await profile['mine_start_ws'].send_json(
        #             {"size": size, "bomb_coords": bomb_coords, "history": history}
        #         )

    async def broadcast(self, data: dict):
        print(data)
        if data['type'] == 'action':
            history = []
            for history_str in r.lrange(history_key, 0, -1):
                history.append(json.loads(history_str))

            response_data = {**data, "history": history}

            for profile_str in r.lrange(profiles_key, 0, -1):
                profile = json.loads(profile_str)
                if profile['sid'] in self.websockets:
                    await self.websockets[profile['sid']].send_json(response_data)
        elif data['type'] == 'disconnect':
            await self.disconnect(data['sid'])

    async def worker(self):
        for message in pubsub.listen():
            print(os.getpid(), message)
            if message['type'] == 'message':
                data = json.loads(message['data'])
                if data['type'] == 'mine_reset':
                    await self.mine_reset()
                elif data['type'] == 'action':
                    await self.broadcast(data)
                elif data['type'] == 'disconnect':
                    # r.delete(data['sid'])
                    # await self.broadcast({"type": "disconnect", "sid": data['sid']})
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
            # print(data)
            if data['type'] == "start":
                # print('start')
                # r.publish('mine', json.dumps(data))
                await connection_manager.mine_start(websocket)
            elif data['type'] == "players":
                await connection_manager.mine_players()
            elif data['type'] == "action":
                sid = data['sid']
                await connection_manager.mine_action(websocket, sid, data)
            elif data['type'] == 'reset':
                game_reset()
                r.publish(
                    'mine',
                    json.dumps(
                        {
                            "type": "mine_reset",
                            "size": get_redis_size(),
                            "bomb_coords": get_redis_bomb_coords(),
                            "history": [],
                        }
                    ),
                )
                # await connection_manager.mine_reset(websocket)

    except WebSocketDisconnect:
        r.delete(sid)
        list_values = r.lrange(profiles_key, 0, -1)
        for value in list_values:
            if json.loads(value)['sid'] == sid:
                r.lrem(profiles_key, 0, value)
        r.publish('mine', json.dumps({"type": "disconnect", "sid": sid}))
        await connection_manager.broadcast({"type": "disconnect", "sid": sid})

    return


# res = pubsub.get_message()
# print(os.getpid(), res)
# import time

# while True:
#     res = pubsub.get_message()
#     print(os.getpid(), res)
#     time.sleep(1)

# @router.websocket("/ws/mine_players")
# async def mine_players(websocket: WebSocket):
#     await websocket.accept()
#     sid = await websocket.receive_text()
#     await connection_manager.mine_players(websocket, sid)


# @router.websocket("/ws/mine_start/{client_sid}")
# async def mine_start(websocket: WebSocket, client_sid: str):
#     await websocket.accept()
#     await connection_manager.mine_start(websocket, client_sid)


# @router.websocket("/ws/mine_action/{client_sid}")
# async def mine_action(websocket: WebSocket, client_sid: str):
#     await websocket.accept()
#     await connection_manager.mine_action(websocket, client_sid)


# @router.websocket("/ws/mine_restart")
# async def mine_restart(websocket: WebSocket):
#     await websocket.accept()
#     await connection_manager.mine_restart(websocket)


# @router.websocket("leave_mine")
# async def leave_mine(sid):
#     del players[sid]
#     await sm.emit("mine_players", list(players.values()))
#
#
# @router.websocket("disconnect")
# async def disconnect(sid):
#     del players[sid]
#     await sm.emit("mine_players", list(players.values()))
#
#
# @router.websocket("mine_start")
# async def mine_start(sid):
#     await sm.emit("mine_start", {"size": size, "bomb_coords": bomb_coords, "history": history}, room=sid)
#
#
# @router.websocket("mine_restart")
# async def mine_restart(sid):
#     game_restart()
#     await sm.emit("mine_start", {"size": size, "bomb_coords": bomb_coords, "history": history})
#
#
# @router.websocket("mine_reveal")
# async def mine_reveal(sid, data):
#     response_data = {
#         "x": data["x"],
#         "y": data["y"],
#         "name": players[sid]["name"],
#         "color": players[sid]["color"],
#         "action": "reveal",
#     }
#     history.append(response_data)
#     await sm.emit("mine_reveal", {**data, "history": history})
#
#
# @router.websocket("mine_flag")
# async def mine_flag(sid, data):
#     response_data = {
#         "x": data["x"],
#         "y": data["y"],
#         "name": players[sid]["name"],
#         "color": players[sid]["color"],
#         "action": "flag",
#     }
#     history.append(response_data)
#     await sm.emit("mine_flag", {**response_data, "history": history})
