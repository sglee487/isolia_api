from datetime import datetime

from asyncpg import UniqueViolationError
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from decouple import config
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from database.db import database
from database.models.board import board
from database.models.enums import BoardType
from schemas.base import EmailField


class BoardDBManager:

    @staticmethod
    async def post_board(board_type: BoardType, title: str, content: str | None, user_id: int):
        try:
            update_data = {
                "board_type": board_type.value,
                "title": title,
                "content": content,
                "user_id": user_id,
            }
            id_ = await database.execute(
                board.insert()
                .values(update_data)
            )
            return id_
        except Exception as e:
            return JSONResponse(content=e, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
