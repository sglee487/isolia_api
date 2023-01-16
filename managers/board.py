import uuid

from datetime import datetime
from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib.context import CryptContext
from google.auth.transport import requests as google_requests
from google.oauth2.id_token import verify_oauth2_token
from decouple import config

from database.user import UserDBManager
from managers.auth import AuthManager
from database.models.enums import LoginType, RoleType
from services.s3 import S3Service
from utils.user import generate_random_name, generate_profile_urls

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

google_request = google_requests.Request()
s3 = S3Service()


class BoardManager:

    @staticmethod
    async def upload_images(files):
        picture_32, picture_96 = await generate_profile_urls(file=file.file)
        return {
            "picture_32": picture_32,
            "picture_96": picture_96,
        }
