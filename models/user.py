from pydantic import BaseModel, Field
from datetime import datetime

from utils.utils import generate_random_name


class User(BaseModel):
    login_type: str
    email: str
    sns_sub: str
    password: str
    display_name: str = Field(default_factory=generate_random_name)
    role: str
    is_active: bool
    created_at: str = Field(default_factory=datetime.now)
    updated_at: str = Field(default_factory=datetime.now)
    deleted_at: str | None = Field()
