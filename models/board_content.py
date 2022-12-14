import sqlalchemy

from db import metadata

user = sqlalchemy.Table(
    "board_contents",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("board_id", sqlalchemy.ForeignKey("boards.id")),
    sqlalchemy.Column("content", sqlalchemy.Text),
)
