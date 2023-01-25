from datetime import datetime

from asyncpg import UniqueViolationError
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from decouple import config
from sqlalchemy import select
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from database.db import database
from database.models import user, board, comment
from database.models.enums import BoardType
from schemas.base import EmailField


class BoardDBManager:

    @staticmethod
    async def get_post(post_id:int):
        query = select([board, user]).where(board.c.id == post_id).select_from(board.outerjoin(user, board.c.user_id == user.c.id))
        board_data = await database.fetch_one(query)
        comment_query = select([comment, user]).where(comment.c.board_id == post_id).select_from(comment.outerjoin(user, comment.c.user_id == user.c.id))
        comment_data = await database.fetch_all(comment_query)
        return {
            **board_data,
            "comments": comment_data
        }

    @staticmethod
    async def get_board(board_type: BoardType = None, page: int = 1, page_size: int = 10):
        query = select([board, user]).select_from(board.outerjoin(user, board.c.user_id == user.c.id))
        query = query.where(board.c.is_active)
        if board_type:
            query = query.where(board.c.board_type == board_type)
        query = query.order_by(board.c.created_at.desc())

        start = (page - 1) * page_size
        end = page * page_size
        query = query.limit(end).offset(start)
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
