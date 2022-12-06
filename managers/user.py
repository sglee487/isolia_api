from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib.context import CryptContext
from google.auth import jwt
from decouple import config
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from db import database
from managers.auth import AuthManager
from models import user, LoginType, RoleType
from utils.utils import generate_random_name


from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_response(user_data, sns_token=None):
    token = await AuthManager.encode_token(user_data) if not sns_token else sns_token
    return {
        "token": token,
        "login_type": user_data["login_type"].name,
        "email": user_data["email"],
        "display_name": user_data["display_name"],
        "role": user_data["role"].name,
    }


class UserManager:

    @staticmethod
    async def register(user_data):
        user_data["password"] = pwd_context.hash(user_data["password"])
        user_data["is_active"] = True
        try:
            id_ = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(HTTP_400_BAD_REQUEST, "User with this login type & email already exists")
        user_do = await database.fetch_one(user.select().where(user.c.id == id_))
        return await get_user_response(user_do)

    @staticmethod
    async def login(user_data):
        if user_data["login_type"] == LoginType.email:
            user_do = await database.fetch_one(
                user.select().where(user.c.email == user_data["email"]).where(user.c.login_type == LoginType.email))
            if not user_do:
                raise HTTPException(HTTP_400_BAD_REQUEST, "Wrong email or password")
            elif not pwd_context.verify(user_data["password"], user_do["password"]):
                raise HTTPException(HTTP_400_BAD_REQUEST, "Wrong email or password")
            elif not user_do['is_active']:
                raise HTTPException(HTTP_400_BAD_REQUEST, "User is not active")
            return await get_user_response(user_do)

        if user_data["login_type"] == LoginType.google:
            google_credential = jwt.decode(user_data["sns_token"], verify=False)
            if google_credential['aud'] != config("GOOGLE_CLIENT_ID"):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Invalid authentication credentials"
                )
            google_token = user_data["sns_token"]
            user_do = await database.fetch_one(
                user.select().where(user.c.email == google_credential["email"]).where(user.c.login_type == LoginType.google))
            if not user_do:
                user_data = {
                    "login_type": LoginType.google,
                    "sns_sub": google_credential["sub"],
                    "email": google_credential["email"],
                    "display_name": generate_random_name(),
                    "role": RoleType.user,
                    "is_active": True
                }
                id_ = await database.execute(user.insert().values(**user_data))
                user_do = await database.fetch_one(user.select().where(user.c.id == id_))
            elif not user_do['is_active']:
                raise HTTPException(HTTP_400_BAD_REQUEST, "User is not active")
            return await get_user_response(user_do, google_token)

        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid"
        )

    @staticmethod
    async def refresh_token(user_data):
        return await get_user_response(user_data)

    @staticmethod
    async def update(user_data, current_user):
        if not pwd_context.verify(user_data["password"], current_user["password"]):
            raise HTTPException(403, "Wrong password")

        await database.execute(
            user.update().
            where(user.c.id == current_user["id"]).
            values(display_name=user_data["display_name"]))

        if len(user_data["new_password"]) >= 8:
            await database.execute(
                user.update().
                where(user.c.id == current_user["id"]).
                values(password=pwd_context.hash(user_data["new_password"])))

        return {
            "display_name": user_data["display_name"]
        }
