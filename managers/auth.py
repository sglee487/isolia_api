from datetime import datetime, timedelta

import jwt
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from databases.interfaces import Record

from database.user import UserDBManager
from database.models.enums import LoginType


class AuthManager:
    @staticmethod
    def encode_token(user_data) -> (str, datetime):
        try:
            exp = int((datetime.now() + timedelta(hours=8)).timestamp())
            payload = {
                "login_type": user_data["login_type"].value,
                "email": user_data["email"],
                "id": user_data["id"],
                "exp": exp,
            }
            return jwt.encode(payload, config("SECRET_KEY"), algorithm="HS256"), exp
        except Exception as ex:
            # TODO: log
            raise ex

    @staticmethod
    def decode_token(credentials):
        try:
            payload = jwt.decode(
                credentials, config("SECRET_KEY"), algorithms=["HS256"]
            )
            payload['login_type'] = LoginType(payload['login_type'])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(HTTP_401_UNAUTHORIZED, "Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(HTTP_401_UNAUTHORIZED, "Invalid token")

    @staticmethod
    async def get_userdata_from_auth_token(credentials) -> (Record, str):
        payload = AuthManager.decode_token(credentials)
        user_do = await UserDBManager.get_user(LoginType(payload["login_type"]), payload["email"])
        if user_do is None:
            raise HTTPException(HTTP_401_UNAUTHORIZED, "Invalid token")
        return user_do, payload["exp"]


class AppHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> None:
        res = await super().__call__(request)
        if res.credentials != config("APP_KEY"):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Invalid authentication credentials",
            )


class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        res = await super().__call__(request)
        user_do, exp = await AuthManager.get_userdata_from_auth_token(res.credentials)
        request.state.user = user_do
        request.state.token = res.credentials
        request.state.exp = exp
        return res


oauth2_app = AppHTTPBearer()
oauth2_scheme = CustomHTTPBearer()
