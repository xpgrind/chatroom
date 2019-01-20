"""create_message_table

Revision ID: 54cc8e7fb244
Revises: eeabcbb77454
Create Date: 2019-01-17 21:11:04.566691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54cc8e7fb244'
down_revision = 'eeabcbb77454'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'message',
        sa.Column('message_id', sa.Integer, primary_key=True),
        sa.Column('client_message_id', sa.Integer),
        sa.Column('message', sa.Unicode(250)),
        sa.Column('receiver_id', sa.Integer),
        sa.Column('sender_id', sa.Integer),
        sa.Column('client_time', sa.DateTime),
        sa.Column('server_time', sa.DateTime)
    )

def downgrade():
    op.drop_table('message')
