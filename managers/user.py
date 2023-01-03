import uuid

from datetime import datetime
from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib.context import CryptContext
from google.auth.transport import requests as google_requests
from google.oauth2.id_token import verify_oauth2_token
from decouple import config
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from database.user import create_user, get_user, delete_user, update_user
from managers.auth import AuthManager
from models.enums import LoginType, RoleType
from services.s3 import S3Service
from utils.users import generate_random_name, generate_profile_urls

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

google_request = google_requests.Request()
s3 = S3Service()


class UserManager:

    @staticmethod
    async def get_user_response(user_data):
        return {
            "token": user_data["token"],
            "exp": user_data["exp"],
            "login_type": user_data["login_type"],
            "email": user_data["email"],
            "picture_32": user_data["picture_32"],
            "picture_96": user_data["picture_96"],
            "display_name": user_data["display_name"],
            "role": user_data["role"],
        }

    @staticmethod
    async def register(user_data):
        user_data["login_type"] = user_data["login_type"].value
        try:
            user_response = await create_user(
                {
                    **user_data,
                    "password": pwd_context.hash(user_data["password"]),
                    "role": RoleType.user.value,
                    "is_active": True,
                    "created_at": datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                    "updated_at": datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                    "deleted_at": None,
                    "id": str(uuid.uuid4()),
                }
            )
        except UniqueViolationError:
            raise HTTPException(
                HTTP_400_BAD_REQUEST, "User with this login type & email already exists"
            )
        # user_do = await database.fetch_one(user.select().where(user.c.id == id_))
        token, exp = AuthManager.encode_token(user_response)
        return await UserManager.get_user_response({**user_response, "token": token, "exp": exp})

    @staticmethod
    async def login(user_data):
        if user_data["login_type"] == LoginType.email:
            user_do = await get_user(user_data["login_type"], user_data["email"])
            if not user_do:
                raise HTTPException(HTTP_400_BAD_REQUEST, "Wrong email or password")
            elif not pwd_context.verify(user_data["password"], user_do["password"]):
                raise HTTPException(HTTP_400_BAD_REQUEST, "Wrong email or password")
            elif not user_do["is_active"]:
                raise HTTPException(HTTP_400_BAD_REQUEST, "User is not active")
            token, exp = AuthManager.encode_token(user_do)
            return await UserManager.get_user_response({**user_do, "token": token, "exp": exp})

        if user_data["login_type"] == LoginType.google:
            google_credential = verify_oauth2_token(user_data["sns_token"], google_request)
            if google_credential["aud"] != config("GOOGLE_CLIENT_ID"):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Invalid authentication credentials",
                )
            user_do = await get_user(user_data["login_type"], google_credential["email"])
            if not user_do:
                picture_32, picture_96 = await generate_profile_urls(google_credential["picture"].split('=')[0])
                user_do = await create_user({
                    "picture_32": picture_32,
                    "picture_96": picture_96,
                    "login_type": LoginType.google.value,
                    "sns_sub": google_credential["sub"],
                    "email": google_credential["email"],
                    "display_name": generate_random_name(),
                    "role": RoleType.user.value,
                    "is_active": True,
                    "created_at": datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                    "updated_at": datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                    "deleted_at": None,
                    "id": str(uuid.uuid4())
                })
            elif not user_do["is_active"]:
                raise HTTPException(HTTP_400_BAD_REQUEST, "User is not active")
            token, exp = AuthManager.encode_token(user_do)
            return await UserManager.get_user_response({**user_do, "token": token, "exp": exp})

        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid")

    @staticmethod
    async def update(user_update_data, current_user, token, exp):
        if current_user['login_type'] == 'email' and not pwd_context.verify(user_update_data["password"], current_user["password"]):
            raise HTTPException(403, "Wrong password")

        update_data = {
                "login_type": LoginType[current_user["login_type"]],
                "email": current_user["email"],
                "display_name": user_update_data["display_name"]
            }
        if current_user['login_type'] == 'email':
            update_data["password"] = pwd_context.hash(user_update_data["new_password"]) if user_update_data["new_password"] != "" \
                else current_user["password"]

        user_do = await update_user(update_data)

        return await UserManager.get_user_response({**user_do, "token": token, "exp": exp})
