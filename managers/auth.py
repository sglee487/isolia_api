from datetime import datetime, timedelta

import jwt
from google.auth import jwt as google_jwt
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from databases.interfaces import Record

# from db import database
from database.user import create_user, get_user, delete_user, update_user
from models.enums import LoginType, RoleType


class AuthManager:
    @staticmethod
    def encode_token(user_data) -> (str, datetime):
        try:
            exp = int((datetime.now() + timedelta(hours=8)).timestamp())
            payload = {
                "login_type": user_data["login_type"],
                "email": user_data["email"],
                "id": user_data["id"],
                "exp": exp,
            }
            return jwt.encode(payload, config("SECRET_KEY"), algorithm="HS256"), exp
        except Exception as ex:
            # TODO: log
            raise ex
#
#     @staticmethod
#     def decode_token(credentials):
#         try:
#             payload = jwt.decode(
#                 credentials, config("SECRET_KEY"), algorithms=["HS256"]
#             )
#             return payload
#         except jwt.ExpiredSignatureError:
#             raise HTTPException(HTTP_401_UNAUTHORIZED, "Token is expired")
#         except jwt.InvalidTokenError:
#             try:
#                 payload = google_jwt.decode(credentials, verify=False)
#                 return payload
#             except google_jwt.exceptions.RefreshError:
#                 raise HTTPException(HTTP_401_UNAUTHORIZED, "Token is expired")
#             except Exception:
#                 raise HTTPException(HTTP_401_UNAUTHORIZED, "Invalid token")
#
    @staticmethod
    async def get_userdata_from_auth_token(credentials) -> (Record, str):
        try:
            payload = jwt.decode(
                credentials, config("SECRET_KEY"), algorithms=["HS256"]
            )
            user_do = await get_user(LoginType(payload["login_type"]), payload["email"])
            if user_do['id'] != payload['id']:
                raise HTTPException(HTTP_401_UNAUTHORIZED, "Invalid token")
            return user_do, payload["exp"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(HTTP_401_UNAUTHORIZED, "Token is expired")
        except jwt.InvalidTokenError:
            try:
                payload = google_jwt.decode(credentials, verify=False)
                user_do = await get_user(LoginType.google, payload["email"])
                return user_do, payload["exp"]
            except google_jwt.exceptions.RefreshError:
                raise HTTPException(HTTP_401_UNAUTHORIZED, "Token is expired")
            except Exception as ex:
                print(ex)
                raise HTTPException(HTTP_401_UNAUTHORIZED, "Invalid token")


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
