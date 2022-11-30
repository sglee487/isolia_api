from fastapi import Query

from models import LoginType
from schemas.base import UserBase


class UserRegisterIn(UserBase):
    login_type: LoginType
    password: str
    display_name: str


class UserSignIn(UserBase):
    password: str
