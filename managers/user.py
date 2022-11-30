from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib.context import CryptContext

from db import database
from managers.auth import AuthManager
from models import user, LoginType

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data):
        user_data["password"] = pwd_context.hash(user_data["password"])
        try:
            id_ = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "User with this login type & email already exists")
        user_do = await database.fetch_one(user.select().where(user.c.id == id_))
        return {
            "token": await AuthManager.encode_token(user_do),
            "login_type": user_data["login_type"].name,
            "email": user_data["email"],
            "display_name": user_data["display_name"],
            "role": user_data["role"].name,
        }

    @staticmethod
    async def login(user_data):
        user_do = await database.fetch_one(
            user.select().where(user.c.email == user_data["email"]).where(user.c.login_type == LoginType.email))
        if not user_do:
            raise HTTPException(400, "Wrong email or password")
        elif not pwd_context.verify(user_data["password"], user_do["password"]):
            raise HTTPException(400, "Wrong email or password")

        return {
            "token": await AuthManager.encode_token(user_do),
            "login_type": user_do["login_type"].name,
            "email": user_do["email"],
            "display_name": user_do["display_name"],
            "role": user_do["role"].name,
        }
