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


class CommentDBManager:

    @staticmethod
    async def get_comments(post_id: int):
        query = select([comment, user]).where(comment.c.id == post_id).select_from(
            comment.outerjoin(user, comment.c.user_id == user.c.id))
        return await database.fetch_all(query)

    @staticmethod
    async def post_comment(post_id: int, content: str, user_id: int):
        try:
            update_data = {
                "content": content,
                "user_id": user_id,
                "post_id": post_id,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
            id_ = await database.execute(
                comment.insert()
                .values(update_data)
            )
            return id_
        except Exception as e:
            return JSONResponse(content=e, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    # @staticmethod
    # async def delete_comment(comment_id: int):
    #     try:
    #         query = comment.delete().where(comment.c.id == comment_id)
    #         return await database
