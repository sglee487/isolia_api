from schemas.base import UserBase


class UserSignOut(UserBase):
    token: str
    login_type: str
    email: str
    display_name: str
    role: str