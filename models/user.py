import sqlalchemy
from sqlalchemy import UniqueConstraint

from db import metadata
from models.enums import RoleType, LoginType

user = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("sns_sub", sqlalchemy.String(60)),
    sqlalchemy.Column("login_type", sqlalchemy.Enum(LoginType), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(120), nullable=False),
    UniqueConstraint("login_type", "email", name="type_email"),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
    sqlalchemy.Column("display_name", sqlalchemy.String(120), nullable=False, server_default="ㅇㅇ"),
    sqlalchemy.Column("role", sqlalchemy.Enum(RoleType), nullable=False, server_default=RoleType.user.name),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean, nullable=False)
)
