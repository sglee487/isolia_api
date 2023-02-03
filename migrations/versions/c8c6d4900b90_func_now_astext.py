"""func now astext

Revision ID: c8c6d4900b90
Revises: 3b60d6cb3df8
Create Date: 2023-02-03 10:07:39.985695

"""
from datetime import datetime
from pytz import timezone

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c8c6d4900b90'
down_revision = '3b60d6cb3df8'
branch_labels = None
depends_on = None

offset = timezone("Asia/Seoul").utcoffset(datetime.now())
offset_str = f"{offset.seconds // 3600:+03d}:00"


def upgrade() -> None:
    op.alter_column('users', 'created_at',
                    server_default=sa.sql.text(f"'UTC{offset_str}'"))
    op.alter_column('users', 'updated_at',
                    server_default=sa.sql.text(f"'UTC{offset_str}'"))
    op.alter_column('board', 'created_at',
                    server_default=sa.sql.text(f"'UTC{offset_str}'"))
    op.alter_column('board', 'updated_at',
                    server_default=sa.sql.text(f"'UTC{offset_str}'"))
    op.alter_column('comment', 'created_at',
                    server_default=sa.sql.text(f"'UTC{offset_str}'"))
    op.alter_column('comment', 'updated_at',
                    server_default=sa.sql.text(f"'UTC{offset_str}'"))


def downgrade() -> None:
    op.alter_column('users', 'created_at',
                    server_default=sa.sql.expression.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('users', 'updated_at',
                    server_default=sa.sql.expression.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('board', 'created_at',
                    server_default=sa.sql.expression.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('board', 'updated_at',
                    server_default=sa.sql.expression.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('comment', 'created_at',
                    server_default=sa.sql.expression.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('comment', 'updated_at',
                    server_default=sa.sql.expression.text(f'now() at time zone \'UTC{offset_str}\''))
