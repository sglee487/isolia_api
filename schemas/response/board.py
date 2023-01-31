from datetime import datetime
from pydantic import BaseModel

from schemas.base import BoardBase
from schemas.response.comment import CommentListOutResponse
from database.models.enums import BoardType


class BoardListOutResponse(BoardBase):
    comment_count: int
    created_at: datetime
    deleted_at: datetime | None
    like: int
    dislike: int
    display_name: str
    hits: int
    id: int
    is_active: bool
    picture_32: str
    preview_image: str | None
    preview_text: str | None
    updated_at: datetime
    user_id: int


class PostResponse(BoardBase):
    created_at: datetime
    updated_at: datetime
    comments: list[CommentListOutResponse]
    content: str
    display_name: str
    dislike: int
    hits: int
    is_active: bool
    like: int
    picture_96: str
    user_id: int
    user_is_active: bool
