"""server_default UTC+9 with sa.sql.expression.text

Revision ID: 3b60d6cb3df8
Revises: cbe40479d691
Create Date: 2023-02-03 09:59:41.893534

"""
from datetime import datetime
from pytz import timezone

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3b60d6cb3df8'
down_revision = 'cbe40479d691'
branch_labels = None
depends_on = None

offset = timezone("Asia/Seoul").utcoffset(datetime.now())
offset_str = f"{offset.seconds // 3600:+03d}:00"


def upgrade() -> None:
    op.alter_column('users', 'created_at', server_default=sa.sql.expression.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('users', 'updated_at', server_default=sa.sql.expression.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('board', 'created_at', server_default=sa.sql.expression.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('board', 'updated_at', server_default=sa.sql.expression.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('comment', 'created_at', server_default=sa.sql.expression.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('comment', 'updated_at', server_default=sa.sql.expression.text(f'now() at time zone \'UTC{offset_str}\''))


def downgrade() -> None:
    op.alter_column('users', 'created_at', server_default=sa.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('users', 'updated_at', server_default=sa.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('board', 'created_at', server_default=sa.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('board', 'updated_at', server_default=sa.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('comment', 'created_at', server_default=sa.text(f'now() at time zone \'UTC{offset_str}\''))
    op.alter_column('comment', 'updated_at', server_default=sa.text(f'now() at time zone \'UTC{offset_str}\''))
