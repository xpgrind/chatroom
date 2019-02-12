"""Create profile pic table

Revision ID: 572045d0ac6d
Revises: ce7dc349eca5
Create Date: 2019-02-10 22:29:23.893709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '572045d0ac6d'
down_revision = 'ce7dc349eca5'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
        'profile_pic',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('user', sa.Integer, sa.ForeignKey('account.id'), nullable=False),
        sa.Column('path', sa.Text, nullable=False),
        sa.Column('name', sa.String(30)),
    )

def downgrade():
    op.drop_table('profile_pic')
