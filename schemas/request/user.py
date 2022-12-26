import uuid

from pydantic import BaseModel, Field
from datetime import datetime
from pytz import timezone

from models import LoginType
from schemas.base import UserBase, PasswordField

from utils.utils import generate_random_name
from models import LoginType, RoleType


class UserRegisterIn(UserBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    login_type: str # LoginType
    password: PasswordField
    display_name: str = Field(default_factory=generate_random_name)
    role: str = RoleType.user.name # RoleType
    is_active: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d_%H-%M-%S"))
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d_%H-%M-%S"))
    deleted_at: str | None = Field()


class UserUpdateIn(UserBase):
    display_name: str
    password: PasswordField
    new_password: PasswordField


class UserSignIn(UserBase):
    login_type: LoginType
    password: PasswordField | None
    sns_token: str | None
