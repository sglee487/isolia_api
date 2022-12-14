import sqlalchemy

from db import metadata

board_content = sqlalchemy.Table(
    "board_contents",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("content", sqlalchemy.Text),
)
