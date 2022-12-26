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
from models import user


class AuthManager:
    @staticmethod
    def encode_token(user_data) -> (str, datetime):
        try:
            exp = int((datetime.utcnow() + timedelta(hours=8)).timestamp())
            payload = {
                "sub": user_data["id"],
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
#     @staticmethod
#     async def get_userdata_from_auth_token(credentials) -> (Record, str):
#         try:
#             payload = jwt.decode(
#                 credentials, config("SECRET_KEY"), algorithms=["HS256"]
#             )
#             user_do = await database.fetch_one(
#                 user.select().where(user.c.id == payload["sub"])
#             )
#             return user_do, payload["exp"]
#         except jwt.ExpiredSignatureError:
#             raise HTTPException(HTTP_401_UNAUTHORIZED, "Token is expired")
#         except jwt.InvalidTokenError:
#             try:
#                 payload = google_jwt.decode(credentials, certs=config("GOOGLE_CLIENT_ID"))
#                 user_do = await database.fetch_one(
#                     user.select().where(user.c.sns_sub == payload["sub"])
#                 )
#                 return user_do, payload["exp"]
#             except google_jwt.exceptions.RefreshError:
#                 raise HTTPException(HTTP_401_UNAUTHORIZED, "Token is expired")
#             except Exception as ex:
#                 print(ex)
#                 raise HTTPException(HTTP_401_UNAUTHORIZED, "Invalid token")


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
