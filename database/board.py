from pytz import timezone

from asyncpg import UniqueViolationError
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from decouple import config
from sqlalchemy import select, func
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from database.db import database
from database.models import user, board, comment
from database.models.enums import BoardType
from schemas.base import EmailField


class BoardDBManager:

    @staticmethod
    async def get_post(post_id: int):
        # update hits in board
        query = board.update().where(board.c.id == post_id).values(hits=board.c.hits + 1)
        await database.execute(query)

        # get post with user info, comment data
        query = select([board.c.id, board.c.board_type, board.c.title, board.c.created_at.label("created_at"),
                        board.c.updated_at.label("updated_at"), board.c.hits, board.c.content, board.c.like,
                        board.c.dislike, board.c.is_active.label("is_active"), user.c.id.label("user_id"), user.c.picture_96,
                        user.c.display_name, user.c.is_active.label("user_is_active")]).where(board.c.id == post_id).select_from(
            board.outerjoin(user, board.c.user_id == user.c.id))
        board_data = await database.fetch_one(query)
        comment_query = select(
            [comment.c.id, comment.c.content, comment.c.created_at, comment.c.updated_at,
             comment.c.like, comment.c.is_active, user.c.id.label("user_id"),
             user.c.picture_96, user.c.display_name, user.c.is_active.label("user_is_active")]).where(
            comment.c.board_id == post_id).select_from(
            comment.outerjoin(user, comment.c.user_id == user.c.id))
        comment_data = await database.fetch_all(comment_query)
        return {
            **board_data,
            "comments": comment_data
        }

    @staticmethod
    async def get_board(board_type: BoardType = None, page: int = 1, page_size: int = 10):
        c_query = select([comment.c.board_id, func.count(comment.c.id).label("comment_count")]).group_by(
            comment.c.board_id)
        query = select([board, user.c.display_name, user.c.picture_32,
                        func.coalesce(c_query.c.comment_count, 0).label("comment_count")]).select_from(
            board.outerjoin(user, board.c.user_id == user.c.id).join(c_query, board.c.id == c_query.c.board_id,
                                                                     isouter=True))
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
    async def post_board(board_type: BoardType, title: str, content: str | None, preview_text: str | None,
                         preview_image: str | None, user_id: int):
        try:
            update_data = {
                "board_type": board_type.value,
                "title": title,
                "content": content,
                "preview_text": preview_text,
                "preview_image": preview_image,
                "user_id": user_id,
            }
            id_ = await database.execute(
                board.insert()
                .values(update_data)
            )
            return id_
        except Exception as e:
            return JSONResponse(content=e, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    # @staticmethod
    # async def update_board(board_id: int, title: str, content: str | None, preview_text: str | None, preview_image: str | None, user_id: int):
    #     try:
    #         update_data = {
    #             "title": title,
    #             "content": content,
    #             "preview_text": preview_text,
    #             "preview_image": preview_image,
    #             "user_id": user_id,
    #             "updated_at": datetime.now(),
    #         }
    #         id_ = await database.execute(
    #             board.update()
    #             .where(board.c.id == board_id)
    #             .values(update_data)
    #         )
    #         return id_
    #     except Exception as e:
    #         return JSONResponse(content=e, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
    #
    # @staticmethod
    # async def delete_board(board_id: int, user_id: int):
    #     try:
    #         id_ = await database.execute(
    #             board.update()
    #             .where(board.c.id == board_id)
    #             .values(is_active=False)
    #         )
    #         return id_
    #     except Exception as e:
    #         return JSONResponse(content=e, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    async def post_comment(board_id: int, content: str, user_id: int):
        try:
            update_data = {
                "board_id": board_id,
                "content": content,
                "user_id": user_id,
            }
            id_ = await database.execute(
                comment.insert()
                .values(update_data)
            )
            return id_
        except Exception as e:
            return JSONResponse(content=e, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
