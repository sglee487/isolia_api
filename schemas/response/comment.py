from datetime import datetime

from schemas.base import CommentBase


class CommentListOutResponse(CommentBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    display_name: str
    like: int
    picture_96: str
    user_id: int
    user_is_active: bool
