"""empty message

Revision ID: d0b3c2488189
Revises: f3b05877c7a4
Create Date: 2017-03-25 20:52:10.119476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0b3c2488189'
down_revision = 'f3b05877c7a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('crimes', sa.Column('asdf', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('crimes', 'asdf')
    # ### end Alembic commands ###
