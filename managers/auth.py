from datetime import datetime, timedelta

import jwt
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from db import database
from models import user


class AuthManager:
    @staticmethod
    async def encode_token(user_data):
        try:
            payload = {
                "sub": user_data["id"],
                "exp": datetime.utcnow() + timedelta(minutes=5)
            }
            return jwt.encode(payload, config("SECRET_KEY"), algorithm="HS256")
        except Exception as ex:
            # TODO: log
            raise ex


class AppHTTPBearer(HTTPBearer):
    async def __call__(
            self, request: Request
    ) -> None:
        res = await super().__call__(request)
        if res.credentials != config("APP_KEY"):
            raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Invalid authentication credentials"
                )


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
            self, request: Request
    ) -> HTTPAuthorizationCredentials | None:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(res.credentials, config("SECRET_KEY"), algorithms=["HS256"])
            user_data = await database.fetch_one(user.select().where(user.c.id == payload["sub"]))
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(HTTP_401_UNAUTHORIZED, "Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(HTTP_401_UNAUTHORIZED, "Invalid token")


oauth2_app = AppHTTPBearer()
oauth2_scheme = CustomHTTPBearer()
