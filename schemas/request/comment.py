from schemas.base import CommentBase


class CommentCreateIn(CommentBase):
    board_id: int
