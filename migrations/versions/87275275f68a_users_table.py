"""users table

Revision ID: 87275275f68a
Revises: 
Create Date: 2020-02-16 01:27:14.344562

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '87275275f68a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
        sa.Column('id', mysql.BIGINT(display_width=20, unsigned=True), autoincrement=True, nullable=False),
        sa.Column('first_name', mysql.VARCHAR(length=255), nullable=False),
        sa.Column('last_name', mysql.VARCHAR(length=255), nullable=False),
        sa.Column('username', mysql.VARCHAR(length=255), nullable=False),
        sa.Column('email', mysql.VARCHAR(length=255), nullable=False),
        sa.Column('social_id', mysql.VARCHAR(length=255), nullable=False),
        sa.Column('social_service', mysql.VARCHAR(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )

    op.create_index('user_index', 'user', ['email'])


def downgrade():
    op.drop_table('user')
    drop_index("user_index")