from pydantic import Field

from schemas.base import UserBase, ProfilePictureBase, PasswordField, NewPasswordField
from utils.user import generate_random_name


class UserRegisterIn(UserBase):
    password: PasswordField
    display_name: str = Field(default_factory=generate_random_name)


class UserUpdateIn(UserBase, ProfilePictureBase):
    display_name: str
    password: NewPasswordField
    new_password: NewPasswordField


class UserSignIn(UserBase):
    password: PasswordField | None
    sns_token: str | None
