import sqlalchemy as sa

from src.configurator import config
from src.database.sql import Base

__all__ = ("User",)


class User(Base):
    __tablename__ = config.database.sql.tables.users

    id = sa.Column("id", sa.Integer, nullable=False, primary_key=True)
    created_at = sa.Column("created_at", sa.DateTime, nullable=False, default=sa.func.now())
