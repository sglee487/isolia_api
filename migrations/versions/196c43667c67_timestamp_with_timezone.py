"""timestamp with timezone'

Revision ID: 196c43667c67
Revises: 0548f090a331
Create Date: 2023-02-06 21:11:29.158006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '196c43667c67'
down_revision = '0548f090a331'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'created_at', existing_type=sa.TIMESTAMP(), type_=sa.TIMESTAMP(timezone=True))
    op.alter_column('users', 'updated_at', existing_type=sa.TIMESTAMP(), type_=sa.TIMESTAMP(timezone=True))
    op.alter_column('board', 'created_at', existing_type=sa.TIMESTAMP(), type_=sa.TIMESTAMP(timezone=True))
    op.alter_column('board', 'updated_at', existing_type=sa.TIMESTAMP(), type_=sa.TIMESTAMP(timezone=True))
    op.alter_column('comment', 'created_at', existing_type=sa.TIMESTAMP(), type_=sa.TIMESTAMP(timezone=True))
    op.alter_column('comment', 'updated_at', existing_type=sa.TIMESTAMP(), type_=sa.TIMESTAMP(timezone=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'created_at', existing_type=sa.TIMESTAMP(timezone=True), type_=sa.TIMESTAMP())
    op.alter_column('users', 'updated_at', existing_type=sa.TIMESTAMP(timezone=True), type_=sa.TIMESTAMP())
    op.alter_column('board', 'created_at', existing_type=sa.TIMESTAMP(timezone=True), type_=sa.TIMESTAMP())
    op.alter_column('board', 'updated_at', existing_type=sa.TIMESTAMP(timezone=True), type_=sa.TIMESTAMP())
    op.alter_column('comment', 'created_at', existing_type=sa.TIMESTAMP(timezone=True), type_=sa.TIMESTAMP())
    op.alter_column('comment', 'updated_at', existing_type=sa.TIMESTAMP(timezone=True), type_=sa.TIMESTAMP())
    # ### end Alembic commands ###
