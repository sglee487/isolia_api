import sqlalchemy

from db import metadata
from models.enums import BoardType

user = sqlalchemy.Table(
    "boards",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("board_type", sqlalchemy.Enum(BoardType), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(120), nullable=False),
    sqlalchemy.Column("content", sqlalchemy.Text),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), nullable=False),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), nullable=False),
    sqlalchemy.Column("deleted_at", sqlalchemy.DateTime),
    sqlalchemy.Column("is_deleted", sqlalchemy.Boolean, nullable=False, server_default="0"),
    sqlalchemy.Column("is_notice", sqlalchemy.Boolean, nullable=False, server_default="0"),
)