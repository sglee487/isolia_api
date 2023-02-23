from fastapi import FastAPI, WebSocket
from starlette.middleware.cors import CORSMiddleware

# import socketio
# from fastapi_socketio import SocketManager

# from db import database
# from database.db import create_tables
from database.db import database
from resources.routes import api_router
import redis

# from sockets.minesweeper import sio
from sockets.minesweeper import router as ws_router

origins = [
    "http://localhost",
    "http://127.0.0.1:5173",
    "http://localhost:8001",
    "http://localhost:8000",
    "http://localhost:4200",
    "http://localhost:5173",
    "https://isolia.shop",
]

app = FastAPI()
app.include_router(api_router)
app.include_router(ws_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    r = redis.Redis(host='127.0.0.1', port=6379, db=0, charset="utf-8", decode_responses=True)
    r.flushdb()


# app = socketio.ASGIApp(sio, app)

# socket_manager = SocketManager(app=app)
