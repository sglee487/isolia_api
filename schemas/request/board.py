from schemas.base import BoardBase


class BoardCreateIn(BoardBase):
    content: str
