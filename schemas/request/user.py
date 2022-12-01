from fastapi import Query

from models import LoginType
from schemas.base import UserBase, PasswordField


class UserRegisterIn(UserBase):
    login_type: LoginType
    password: PasswordField
    display_name: str


class UserUpdateIn(UserBase):
    display_name: str
    password: PasswordField
    new_password: PasswordField


class UserSignIn(UserBase):
    password: PasswordField
