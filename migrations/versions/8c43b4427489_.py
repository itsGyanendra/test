"""empty message

Revision ID: 8c43b4427489
Revises: 9e6f6578ca84
Create Date: 2023-08-14 12:05:19.868841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c43b4427489'
down_revision = '9e6f6578ca84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flags', sa.Column('user_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('flags', 'user_id')
    # ### end Alembic commands ###