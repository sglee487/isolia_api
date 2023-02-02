import sqlalchemy
from sqlalchemy import UniqueConstraint

from database.db import metadata
from database.models.enums import BoardType

board = sqlalchemy.Table(
    "board",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("board_type", sqlalchemy.Enum(BoardType), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(120), nullable=False),
    sqlalchemy.Column("content", sqlalchemy.Text),
    sqlalchemy.Column("preview_text", sqlalchemy.Text),
    sqlalchemy.Column("preview_image", sqlalchemy.Text),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("hits", sqlalchemy.Integer, server_default="0"),
    sqlalchemy.Column("like", sqlalchemy.Integer, server_default="0"),
    sqlalchemy.Column("dislike", sqlalchemy.Integer, server_default="0"),
    sqlalchemy.Column(
        "is_active", sqlalchemy.Boolean, nullable=False, server_default="1"
    ),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False,
                      server_default=sqlalchemy.sql.expression.text("NOW() AT TIME ZONE 'UTC+9'")),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, nullable=False,
                      server_default=sqlalchemy.sql.expression.text("NOW() AT TIME ZONE 'UTC+9'")),
    sqlalchemy.Column("deleted_at", sqlalchemy.DateTime),

)
