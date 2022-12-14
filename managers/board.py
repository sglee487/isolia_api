from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib.context import CryptContext
from google.auth import jwt
from decouple import config
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from db import database
from managers.auth import AuthManager
from models import user, LoginType, RoleType, board
from models.enums import BoardType
from utils.utils import generate_random_name

class BoardManager:
    @staticmethod
    async def get_board_list(board_type: BoardType):
        board_list = await database.fetch_all(
            board.select().where(board.c.board_type == board_type)
        )
        return board_list

    @staticmethod
    async def write_board(request, board_type: BoardType):
        user_id = request.state.user_id
        if user_id is None:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="로그인이 필요합니다.")

        board_id = await database.execute(
            board.insert().values(
                board_type=board_type,
                user_id=user_id
            )
        )
        return board_id