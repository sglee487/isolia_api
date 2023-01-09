from pydantic import BaseModel

from schemas.base import UserBase, EmailField
from database.models.enums import LoginType, RoleType




class UserResponse(UserBase):
    token: str
    exp: int
    login_type: LoginType
    email: EmailField
    picture_32: str
    picture_96: str
    display_name: str
    role: RoleType


class UserDisplayNameResponse(BaseModel):
    display_name: str
