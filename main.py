from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import socketio

# from db import database
# from database.db import create_tables
from database.db import database
from resources.routes import api_router
from sockets.minesweeper import sio

origins = [
    "http://localhost",
    "http://127.0.0.1:5173",
    "http://localhost:8001",
    "http://localhost:8000",
    "http://localhost:4200",
    "http://localhost:5173",
    "https://isolia.shop"
]

app = FastAPI()
app.include_router(api_router)
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
async def startup():
    await database.disconnect()

app = socketio.ASGIApp(sio, app)
