import uuid

from datetime import datetime
from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib.context import CryptContext
from google.auth.transport import requests as google_requests
from google.oauth2.id_token import verify_oauth2_token
from decouple import config
from databases.interfaces import Record

from database.board import BoardDBManager
from managers.auth import AuthManager
from database.models.enums import LoginType, RoleType
from schemas.request.board import BoardCreateIn
from services.s3 import S3Service
from utils.board import generate_image_urls

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

google_request = google_requests.Request()
s3 = S3Service()


class BoardManager:

    @staticmethod
    async def upload_images(files, user_id):
        return await generate_image_urls(files, user_id)

    @staticmethod
    async def post_board(board_model: BoardCreateIn, user_id: int):
        return await BoardDBManager.post_board(board_model.board_type, board_model.title, board_model.content, user_id)