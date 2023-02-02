from passlib.context import CryptContext
from google.auth.transport import requests as google_requests
from databases.interfaces import Record
from bs4 import BeautifulSoup

from database.board import BoardDBManager
from database.models.enums import BoardType
from schemas.request.board import BoardCreateIn
from schemas.request.comment import CommentCreateIn
from services.s3 import S3Service
from utils.board import generate_image_urls

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

google_request = google_requests.Request()
s3 = S3Service()


class BoardManager:

    @staticmethod
    async def get_post(post_id: int) -> Record:
        return await BoardDBManager.get_post(post_id)

    @staticmethod
    async def get_board_list(board_type: BoardType | None, page: int) -> list[Record]:
        return await BoardDBManager.get_board(board_type, page)

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

    @staticmethod
    async def post_comment(board_id: int, comment_model: CommentCreateIn, user_id: int):

        return await BoardDBManager.post_comment(board_id, comment_model.content, user_id)
