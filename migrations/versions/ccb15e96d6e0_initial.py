"""initial

Revision ID: ccb15e96d6e0
Revises: 
Create Date: 2022-11-30 15:56:40.028067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccb15e96d6e0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login_type', sa.Enum('email', 'naver', 'google', 'apple', name='logintype'), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('display_name', sa.String(length=120), nullable=False),
    sa.Column('role', sa.Enum('admin', 'user', name='roletype'), server_default='user', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login_type', 'email', name='type_email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
