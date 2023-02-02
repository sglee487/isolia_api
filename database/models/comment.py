import sqlalchemy

from database.db import metadata

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
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False,
                      server_default=sqlalchemy.sql.expression.text("NOW() AT TIME ZONE 'UTC+9'")),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, nullable=False,
                      server_default=sqlalchemy.sql.expression.text("NOW() AT TIME ZONE 'UTC+9'")),
    sqlalchemy.Column("deleted_at", sqlalchemy.DateTime),

)
