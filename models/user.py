import uuid

from pydantic import BaseModel, Field
from datetime import datetime

from utils.utils import generate_random_name
from models import LoginType, RoleType


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    login_type: str # LoginType
    email: str
    sns_sub: str | None
    password: str
    display_name: str = Field(default_factory=generate_random_name)
    role: str # RoleType
    is_active: bool = True
    created_at: str = Field(default_factory=datetime.now)
    updated_at: str = Field(default_factory=datetime.now)
    deleted_at: str | None = Field()
