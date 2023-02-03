"""change created_at column to timestamp with time zone and set default to UTC+9

Revision ID: cbe40479d691
Revises: db300e70a36f
Create Date: 2023-02-03 09:15:08.641317

"""
from datetime import datetime
from pytz import timezone

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cbe40479d691'
down_revision = 'db300e70a36f'
branch_labels = None
depends_on = None

offset = timezone("Asia/Seoul").utcoffset(datetime.now())
offset_str = f"{offset.seconds//3600:+03d}:00"


def upgrade():
    op.alter_column('users', 'created_at', existing_type=sa.TIMESTAMP(), type_=sa.TIMESTAMP(timezone=True),
                    server_default=sa.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('users', 'updated_at', existing_type=sa.TIMESTAMP(), type_=sa.TIMESTAMP(timezone=True),
                    server_default=sa.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('board', 'created_at', existing_type=sa.TIMESTAMP(), type_=sa.TIMESTAMP(timezone=True),
                    server_default=sa.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('board', 'updated_at', existing_type=sa.TIMESTAMP(), type_=sa.TIMESTAMP(timezone=True),
                    server_default=sa.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('comment', 'created_at', existing_type=sa.TIMESTAMP(), type_=sa.TIMESTAMP(timezone=True),
                    server_default=sa.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('comment', 'updated_at', existing_type=sa.TIMESTAMP(), type_=sa.TIMESTAMP(timezone=True),
                    server_default=sa.text(f'now() at time zone \'UTC{offset_str}\''))


def downgrade():
    op.alter_column('users', 'created_at', existing_type=sa.TIMESTAMP(timezone=True), type_=sa.TIMESTAMP(),
                    server_default=sa.text('now() at time zone \'UTC+00:00\''))
    op.alter_column('users', 'updated_at', existing_type=sa.TIMESTAMP(timezone=True), type_=sa.TIMESTAMP(),
                    server_default=sa.text('now() at time zone \'UTC+00:00\''))
    op.alter_column('board', 'created_at', existing_type=sa.TIMESTAMP(timezone=True), type_=sa.TIMESTAMP(),
                    server_default=sa.text('now() at time zone \'UTC+00:00\''))
    op.alter_column('board', 'updated_at', existing_type=sa.TIMESTAMP(timezone=True), type_=sa.TIMESTAMP(),
                    server_default=sa.text('now() at time zone \'UTC+00:00\''))
    op.alter_column('comment', 'created_at', existing_type=sa.TIMESTAMP(timezone=True), type_=sa.TIMESTAMP(),
                    server_default=sa.text('now() at time zone \'UTC+00:00\''))
    op.alter_column('comment', 'updated_at', existing_type=sa.TIMESTAMP(timezone=True), type_=sa.TIMESTAMP(),
                    server_default=sa.text('now() at time zone \'UTC+00:00\''))
