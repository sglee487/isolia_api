from pydantic import BaseModel

from schemas.base import UserBase


class UserResponse(UserBase):
    token: str
    exp: int
    login_type: str
    email: str
    picture_32: str
    picture_96: str
    display_name: str
    role: str


class UserDisplayNameResponse(BaseModel):
    display_name: str
