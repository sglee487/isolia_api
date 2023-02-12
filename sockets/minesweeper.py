import random

from socketio import AsyncServer

from utils.mine import generate_nickname, generate_color

origins = [
    "http://localhost",
    "http://127.0.0.1:5173",
    "http://localhost:8001",
    "http://localhost:8000",
    "http://localhost:4200",
    "http://localhost:5173",
    "https://isolia.shop"
]
sio = AsyncServer(async_mode='asgi', cors_allowed_origins=origins)

size = 12
bombs = 24
bombs_coords = []

players = dict()
sids = []
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


@sio.on("connect")
async def connect(sid, environ):
    sids.append(sid)
    players[sid] = {
        "name": generate_nickname(),
        "color": generate_color(),
    }

    await sio.emit("give_player_info", players[sid], room=sid)
    await sio.emit("mine_players", list(players.values()))
    await sio.emit("mine_history", history)


@sio.event()
async def leave_mine(sid):
    del players[sid]
    await sio.emit("mine_players", list(players.values()))


@sio.on("disconnect")
async def disconnect(sid):
    del players[sid]
    await sio.emit("mine_players", list(players.values()))


@sio.event
async def mine_start(sid):
    await sio.emit("mine_start", {"size": size, "bombs": bombs_coords, "history": history}, room=sid)


@sio.event
async def mine_restart(sid):
    game_restart()
    await sio.emit("mine_start", {"size": size, "bombs": bombs_coords, "history": history})


@sio.event
async def mine_reveal(sid, data):
    response_data = {
        "x": data["x"],
        "y": data["y"],
        "name": players[sid]["name"],
        "color": players[sid]["color"],
        "action": "reveal",
    }
    history.append(response_data)
    await sio.emit("mine_reveal", {**data, "history": history})


@sio.event
async def mine_flag(sid, data):
    response_data = {
        "x": data["x"],
        "y": data["y"],
        "name": players[sid]["name"],
        "color": players[sid]["color"],
        "action": "flag",
    }
    history.append(response_data)
    await sio.emit("mine_flag", {**response_data, "history": history})
