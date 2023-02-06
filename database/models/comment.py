from datetime import datetime
from pytz import timezone

import sqlalchemy

from database.db import metadata

offset = timezone("Asia/Seoul").utcoffset(datetime.now())
offset_str = f"{offset.seconds//3600:+03d}:00"

comment = sqlalchemy.Table(
    "comment",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("content", sqlalchemy.Text),
    sqlalchemy.Column("board_id", sqlalchemy.ForeignKey("board.id")),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("like", sqlalchemy.Integer, server_default="0"),
    sqlalchemy.Column(
        "is_active", sqlalchemy.Boolean, nullable=False, server_default="1"
    ),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), nullable=False,
                      server_default=sqlalchemy.sql.text(f'now() at time zone \'UTC{offset_str}\'')),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True), nullable=False,
                      server_default=sqlalchemy.sql.text(f'now() at time zone \'UTC{offset_str}\'')),
    sqlalchemy.Column("deleted_at", sqlalchemy.DateTime),

)
