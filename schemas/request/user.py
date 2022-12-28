import uuid

from pydantic import BaseModel, Field

from models import LoginType
from schemas.base import UserBase, PasswordField

from utils.utils import generate_random_name
from models import LoginType, RoleType


class UserRegisterIn(UserBase):
    login_type: LoginType
    password: PasswordField
    display_name: str = Field(default_factory=generate_random_name)


class UserUpdateIn(UserBase):
    display_name: str
    password: PasswordField
    new_password: PasswordField


class UserSignIn(UserBase):
    login_type: LoginType
    password: PasswordField | None
    sns_token: str | None
