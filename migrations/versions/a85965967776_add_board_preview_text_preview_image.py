"""add board preview_text, preview_image

Revision ID: a85965967776
Revises: 4e513930c4a7
Create Date: 2023-01-18 09:01:38.686894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a85965967776'
down_revision = '4e513930c4a7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board', sa.Column('preview_text', sa.Text(), nullable=True))
    op.add_column('board', sa.Column('preview_image', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('board', 'preview_image')
    op.drop_column('board', 'preview_text')
    # ### end Alembic commands ###