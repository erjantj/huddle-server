"""source subscription table

Revision ID: f6c83c9f2af5
Revises: 2ae17ba105da
Create Date: 2020-03-07 14:39:48.049768

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f6c83c9f2af5'
down_revision = '2ae17ba105da'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('source_subscription',
        sa.Column('id', mysql.BIGINT(display_width=20, unsigned=True), autoincrement=True, nullable=False),
        sa.Column('user_id', mysql.BIGINT(display_width=20, unsigned=True), nullable=False),
        sa.Column('source_id', mysql.BIGINT(display_width=20, unsigned=True), nullable=False),
        sa.Column('created_at', mysql.TIMESTAMP(), nullable=True),
        sa.Column('updated_at', mysql.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )

  op.create_index('source_subscription_index', 'source_subscription', ['user_id', 'source_id'])


def downgrade():
    op.drop_index("source_subscription_index")
    op.drop_table('source_subscription')
