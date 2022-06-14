import sqlalchemy as sa

from src.configurator import config
from src.database.sql import Base


class State(Base):
    __tablename__ = config.database.sql.tables.states

    id = sa.Column("id", sa.Integer, nullable=False, primary_key=True)
    peer_id = sa.Column("peer_id", sa.Integer, nullable=False, unique=True)
    state = sa.Column("state", sa.String, nullable=False)
    payload = sa.Column("payload", sa.String, nullable=False, server_default="{}")
