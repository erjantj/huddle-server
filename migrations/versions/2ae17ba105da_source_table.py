"""source table

Revision ID: 2ae17ba105da
Revises: 87275275f68a
Create Date: 2020-02-16 18:13:57.405749

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2ae17ba105da'
down_revision = '87275275f68a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('source',
        sa.Column('id', mysql.BIGINT(display_width=20, unsigned=True), autoincrement=True, nullable=False),
        sa.Column('name', mysql.VARCHAR(length=255), nullable=False),
        sa.Column('description', mysql.TEXT(), nullable=False),
        sa.Column('url', mysql.VARCHAR(length=255), nullable=False),
        sa.Column('feed_link', mysql.VARCHAR(length=255), nullable=False),
        sa.Column('icon', mysql.VARCHAR(length=255), nullable=False),
        sa.Column('language', mysql.VARCHAR(length=255), nullable=False),
        sa.Column('created_at', mysql.TIMESTAMP(), nullable=True),
        sa.Column('updated_at', mysql.TIMESTAMP(), nullable=True),
        mysql_engine='InnoDB'
    )

    op.create_index('source_index', 'source', ['created_at', 'updated_at'])


def downgrade():
    op.drop_table('source')
    drop_index("source_index")