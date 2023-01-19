from datetime import datetime

from asyncpg import UniqueViolationError
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from decouple import config
from sqlalchemy import select
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from pytz import timezone

from database.db import database
from database.models import user, board
from database.models.enums import BoardType
from schemas.base import EmailField


class BoardDBManager:

    @staticmethod
    async def get_post(post_id:int):
        query = select([board]).where(board.c.id == post_id)
        return await database.fetch_one(query)

    @staticmethod
    async def get_board(board_type: BoardType = None):
        query = select([board, user]).select_from(board.outerjoin(user, board.c.user_id == user.c.id))
        query = query.where(board.c.is_active)
        if board_type:
            query = query.where(board.c.board_type == board_type)
        query = query.order_by(board.c.created_at.desc())
        result = await database.fetch_all(query)
        return result

    @staticmethod
    async def post_board(board_type: BoardType, title: str, content: str | None, preview_text: str | None, preview_image: str | None, user_id: int):
        try:
            update_data = {
                "board_type": board_type.value,
                "title": title,
                "content": content,
                "preview_text": preview_text,
                "preview_image": preview_image,
                "user_id": user_id,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
            id_ = await database.execute(
                board.insert()
                .values(update_data)
            )
            return id_
        except Exception as e:
            return JSONResponse(content=e, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
