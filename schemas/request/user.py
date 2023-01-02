import uuid

from pydantic import BaseModel, Field

from schemas.base import UserBase, PasswordField, NewPasswordField

from utils.users import generate_random_name
from models.enums import LoginType, RoleType


class UserRegisterIn(UserBase):
    password: PasswordField
    display_name: str = Field(default_factory=generate_random_name)


class UserUpdateIn(UserBase):
    display_name: str
    password: NewPasswordField
    new_password: NewPasswordField


class UserSignIn(UserBase):
    password: PasswordField | None
    sns_token: str | None
