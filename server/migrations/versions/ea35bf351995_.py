"""empty message

Revision ID: ea35bf351995
Revises: d0b3c2488189
Create Date: 2017-03-25 20:52:27.250252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea35bf351995'
down_revision = 'd0b3c2488189'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('crimes', 'asdf')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('crimes', sa.Column('asdf', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
