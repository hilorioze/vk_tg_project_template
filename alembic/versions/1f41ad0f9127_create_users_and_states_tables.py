"""Create users and states tables

Revision ID: 1f41ad0f9127
Revises: 
Create Date: 2022-06-11 08:21:18.194969

"""
from alembic import op
import sqlalchemy as sa
from src.configurator import config


# revision identifiers, used by Alembic.
revision = '1f41ad0f9127'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        config.database.sql.tables.users,
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("created_at", sa.DateTime, nullable=False, default=sa.func.now())
    )
    op.create_table(
        config.database.sql.tables.states,
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("peer_id", sa.Integer, nullable=False, unique=True),
        sa.Column("state", sa.String, nullable=False),
        sa.Column("payload", sa.String, nullable=False, server_default="{}")
    )


def downgrade():
    op.drop_table(
        config.database.sql.tables.users
    )
    op.drop_table(
        config.database.sql.tables.states
    )
