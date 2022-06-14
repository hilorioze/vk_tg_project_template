import typing

import sqlalchemy as sa

from src.database.models import User
from src.database.sql import engine

__all__ = ("UserRepository",)


class UserRepository:
    def __init__(self, id: int):
        self.id = id

    @staticmethod
    async def register(id: int) -> typing.Tuple[bool, typing.Optional[Exception]]:
        async with engine.begin() as conn:
            query = sa.insert(User).values(id=id)
            try:
                await conn.execute(query)
            except Exception as exc:
                await conn.rollback()
                return False, exc
            else:
                await conn.commit()
                return True, None

    async def get_user(self) -> typing.Optional[User]:
        async with engine.begin() as conn:
            query = sa.select(User).where(User.id == self.id)
            result: typing.Optional[User] = (await conn.execute(query)).fetchone()
        return result

    async def edit_user(
        self, **kwargs: typing.Any
    ) -> typing.Tuple[bool, typing.Optional[Exception]]:
        async with engine.begin() as conn:
            query = sa.update(User).where(User.id == self.id).values(**kwargs)
            try:
                await conn.execute(query)
            except Exception as exc:
                await conn.rollback()
                return False, exc
            else:
                await conn.commit()
                return True, None
