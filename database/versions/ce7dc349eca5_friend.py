"""firends

Revision ID: ce7dc349eca5
Revises: eeabcbb77454
Create Date: 2019-02-01 19:13:58.592145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce7dc349eca5'
down_revision = 'eeabcbb77454'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'friend',
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('friend_id', sa.Integer),
        sa.PrimaryKeyConstraint('user_id', 'friend_id', name='mytable_pk')
    )

def downgrade():
    op.drop_table('friend')
