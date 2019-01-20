"""create account table

Revision ID: eeabcbb77454
Revises: 3f1b1367e94d
Create Date: 2019-01-17 20:57:42.955640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeabcbb77454'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(100), nullable=False, unique=True),
        sa.Column('description', sa.Unicode(200)),
        sa.Column('email', sa.String(50), nullable=False, unique=True)
    )


def downgrade():
    op.drop_table('account')
