"""added temstamp

Revision ID: 1be39282ff01
Revises: 
Create Date: 2023-03-24 15:08:30.206298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1be39282ff01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('url_map', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_url_map_timestamp'), 'url_map', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_url_map_timestamp'), table_name='url_map')
    op.drop_column('url_map', 'timestamp')
    # ### end Alembic commands ###
