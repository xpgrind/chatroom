"""create token table

Revision ID: 8ecb94bf73ac
Revises: 54cc8e7fb244
Create Date: 2019-01-31 19:23:35.734439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ecb94bf73ac'
down_revision = '54cc8e7fb244'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'token',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('account.id')),
        sa.Column('token', sa.Text, nullable=False, unique=True),
        sa.Column('create_time', sa.TIMESTAMP, nullable=False, unique=True),
        sa.Column('expire_time', sa.TIMESTAMP, nullable=False, unique=True)
    )

def downgrade():
    op.drop_table('token')
