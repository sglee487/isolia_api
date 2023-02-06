from datetime import datetime
from pytz import timezone

import sqlalchemy

from database.db import metadata
from database.models.enums import BoardType

offset = timezone("Asia/Seoul").utcoffset(datetime.now())
offset_str = f"{offset.seconds//3600:+03d}:00"

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
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), nullable=False,
                      server_default=sqlalchemy.sql.text(f'now() at time zone \'UTC{offset_str}\'')),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True), nullable=False,
                      server_default=sqlalchemy.sql.text(f'now() at time zone \'UTC{offset_str}\'')),
    sqlalchemy.Column("deleted_at", sqlalchemy.DateTime),

)
