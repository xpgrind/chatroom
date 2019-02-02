"""firends

Revision ID: ce7dc349eca5
Revises: 8ecb94bf73ac
Create Date: 2019-02-01 19:13:58.592145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce7dc349eca5'
down_revision = '8ecb94bf73ac'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'friends',
        sa.Column('user_id', sa.Integer),
        sa.Column('friend_id', sa.Integer),
    )

def downgrade():
    op.drop_table('friends')
