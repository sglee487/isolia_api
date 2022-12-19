from asyncpg import UniqueViolationError
from fastapi import HTTPException
from sqlalchemy import func as sqlalchemy_func
from passlib.context import CryptContext
from google.auth import jwt
from decouple import config
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from db import database
from managers.auth import AuthManager
from models import user, LoginType, RoleType, board, board_content
from models.enums import BoardType
from utils.utils import generate_random_name


class BoardManager:
    @staticmethod
    async def get_board_list(board_type: BoardType):
        board_list = await database.fetch_all(
            query=f"select boards.id, boards.board_type, boards.title, boards.created_at, users.display_name from boards, users where boards.board_type = '{board_type.value}' and boards.user_id = users.id and boards.is_deleted = false order by boards.created_at desc"
        )
        return board_list

    @staticmethod
    async def write_board(request, board_type: BoardType, post_data: dict):
        user = request.state.user
        if user is None:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="로그인이 필요합니다.")

        board_content_id = await database.execute(
            board_content.insert().values(content=post_data["content"])
        )

        board_id = await database.execute(
            board.insert().values(
                board_type=board_type,
                title=post_data["title"],
                content_id=board_content_id,
                user_id=user["id"],
                created_at=sqlalchemy_func.now(),
                updated_at=sqlalchemy_func.now(),
                is_deleted=False,
                is_notice=False,
            )
        )

        return await BoardManager.get_board(board_id)

    @staticmethod
    async def get_board(board_id: int):
        board_data = await database.fetch_one(
            board.select().where(board.c.id == board_id)
        )
        board_content_data = await database.fetch_one(
            board_content.select().where(board_content.c.id == board_data["content_id"])
        )

        return {**dict(board_data), "content": board_content_data["content"]}
