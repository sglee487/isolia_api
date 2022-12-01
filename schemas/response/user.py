from pydantic import BaseModel

from schemas.base import UserBase


class UserResponse(UserBase):
    token: str
    login_type: str
    email: str
    display_name: str
    role: str


class UserDisplayNameResponse(BaseModel):
    display_name: str
