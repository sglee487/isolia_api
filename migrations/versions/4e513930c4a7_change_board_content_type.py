"""change board content type

Revision ID: 4e513930c4a7
Revises: db3b140dc939
Create Date: 2023-01-18 08:57:26.040219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e513930c4a7'
down_revision = 'db3b140dc939'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('board', 'content', type_=sa.Text)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('board', 'content', type_=sa.String(length=255))
    # ### end Alembic commands ###
