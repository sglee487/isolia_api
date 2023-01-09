from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# from db import database
# from database.db import create_tables
from database.db import database
from resources.routes import api_router

origins = [
    "http://localhost",
    "http://127.0.0.1:5173",
    "http://localhost:8001",
    "http://localhost:8000",
    "http://localhost:4200",
    "http://localhost:5173",
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
