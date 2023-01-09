import sqlalchemy
from sqlalchemy import UniqueConstraint

from database.db import metadata
from database.models.enums import RoleType, LoginType

user = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("sns_sub", sqlalchemy.String(60)),
    sqlalchemy.Column("login_type", sqlalchemy.Enum(LoginType), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(120), nullable=False),
    UniqueConstraint("login_type", "email", name="type_email"),
    sqlalchemy.Column("picture_32", sqlalchemy.String(255)),
    sqlalchemy.Column("picture_96", sqlalchemy.String(255)),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
    sqlalchemy.Column(
        "display_name", sqlalchemy.String(120), nullable=False, server_default="ㅇㅇ"
    ),
    sqlalchemy.Column(
        "role",
        sqlalchemy.Enum(RoleType),
        nullable=False,
        server_default=RoleType.user.name,
    ),
    sqlalchemy.Column(
        "is_active", sqlalchemy.Boolean, nullable=False, server_default="1"
    ),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("deleted_at", sqlalchemy.DateTime),
)