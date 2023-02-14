import random

from fastapi import APIRouter, WebSocket
import shortuuid
# from socketio import AsyncServer
# from ..main import socket_manager as sm
from starlette.websockets import WebSocketDisconnect

router = APIRouter()

from utils.mine import generate_nickname, generate_color

size = 12
bombs = 24
bombs_coords = []
history = []


def game_restart():
    global bombs_coords, history
    bombs_coords.clear()
    history.clear()

    for i in range(bombs):
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        bombs_coords.append((row, col))


game_restart()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.profiles: dict[str, dict] = dict()

    async def connect(self, websocket: WebSocket):
        self.active_connections.append(websocket)
        sid = shortuuid.uuid()
        self.profiles[sid] = {
            "sid": sid,
            "name": generate_nickname(),
            "color": generate_color(),
        }
        try:
            await websocket.send_json(self.profiles[sid])
            await websocket.receive_text()
        except WebSocketDisconnect:
            if sid in self.profiles:
                del self.profiles[sid]
            await self.disconnect(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        players = []
        for profile in self.profiles.values():
            if 'mine_players_ws' in profile:
                players.append({
                    "name": profile["name"],
                    "color": profile["color"]
                })
        for profile in self.profiles.values():
            if 'mine_players_ws' in profile:
                await profile['mine_players_ws'].send_json(players)

    async def mine_players(self, websocket: WebSocket, sid: str):
        self.profiles[sid]['mine_players_ws'] = websocket
        try:
            while True:
                players = []
                for profile in self.profiles.values():
                    if 'mine_players_ws' in profile:
                        players.append({
                            "name": profile["name"],
                            "color": profile["color"]
                        })
                for profile in self.profiles.values():
                    if 'mine_players_ws' in profile:
                        await profile['mine_players_ws'].send_json(players)
                await websocket.receive_text()

        except WebSocketDisconnect:
            return

    async def mine_start(self, websocket: WebSocket, sid: str):
        self.profiles[sid]['mine_start_ws'] = websocket
        try:
            while True:
                await websocket.send_json({"size": size, "bombs": bombs_coords, "history": history})
                await websocket.receive_text()

        except WebSocketDisconnect:
            return

    async def mine_action(self, websocket: WebSocket, sid: str):
        self.profiles[sid]['mine_action_ws'] = websocket
        try:
            while True:
                data = await websocket.receive_json()
                response_data = {
                    **data,
                    "name": self.profiles[sid]["name"],
                    "color": self.profiles[sid]["color"],
                }
                history.append(response_data)
                for profile in self.profiles.values():
                    if 'mine_action_ws' in profile:
                        await profile['mine_action_ws'].send_json({**response_data, "history": history})

        except WebSocketDisconnect:
            return

    async def mine_restart(self, websocket: WebSocket):
        try:
            while True:
                await websocket.receive_text()
                game_restart()
                for profile in self.profiles.values():
                    if 'mine_start_ws' in profile:
                        await profile['mine_start_ws'].send_json({"size": size, "bombs": bombs_coords, "history": history})

        except WebSocketDisconnect:
            return




connection_manager = ConnectionManager()


@router.websocket("/connect")
async def connect(websocket: WebSocket):
    await websocket.accept()
    await connection_manager.connect(websocket)

@router.websocket("/mine_players")
async def mine_players(websocket: WebSocket):
    await websocket.accept()
    sid = await websocket.receive_text()
    await connection_manager.mine_players(websocket, sid)

@router.websocket("/mine_start/{client_sid}")
async def mine_start(websocket: WebSocket, client_sid: str):
    await websocket.accept()
    await connection_manager.mine_start(websocket, client_sid)

@router.websocket("/mine_action/{client_sid}")
async def mine_action(websocket: WebSocket, client_sid: str):
    await websocket.accept()
    await connection_manager.mine_action(websocket, client_sid)

@router.websocket("/mine_restart")
async def mine_restart(websocket: WebSocket):
    await websocket.accept()
    await connection_manager.mine_restart(websocket)

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
#     await sm.emit("mine_start", {"size": size, "bombs": bombs_coords, "history": history}, room=sid)
#
#
# @router.websocket("mine_restart")
# async def mine_restart(sid):
#     game_restart()
#     await sm.emit("mine_start", {"size": size, "bombs": bombs_coords, "history": history})
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
