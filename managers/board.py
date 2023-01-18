import uuid

from datetime import datetime
from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib.context import CryptContext
from google.auth.transport import requests as google_requests
from google.oauth2.id_token import verify_oauth2_token
from decouple import config
from databases.interfaces import Record
from bs4 import BeautifulSoup

from database.board import BoardDBManager
from managers.auth import AuthManager
from database.models.enums import LoginType, RoleType, BoardType
from schemas.request.board import BoardCreateIn
from services.s3 import S3Service
from utils.board import generate_image_urls

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

google_request = google_requests.Request()
s3 = S3Service()


class BoardManager:

    @staticmethod
    async def get_board_list(board_type: BoardType | None):
        return await BoardDBManager.get_board(board_type)

    @staticmethod
    async def upload_images(files, user_id):
        return await generate_image_urls(files=files, save_root_path=f"board/{user_id}")

    @staticmethod
    async def post_board(post: BoardCreateIn, user_id: int):
        soup = BeautifulSoup(post.content, "html.parser")

        preview_text = soup.text[:120]
        if len(soup.text) > 120:
            preview_text += "..."

        preview_images = await generate_image_urls(urls=[soup.img['src']], size=(256, 192), thumbnail=True,
                                                   save_root_path=f"board/preview/{user_id}") if soup.img else None

        return await BoardDBManager.post_board(post.board_type, post.title, post.content, preview_text,
                                               preview_images[0], user_id)
