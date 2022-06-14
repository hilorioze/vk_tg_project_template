import typing

import sqlalchemy as sa

from src.database.models import State
from src.database.sql import engine
from src.modules import json


class StateRepository:
    @staticmethod
    async def get(peer_id: int) -> typing.Optional[State]:
        async with engine.begin() as conn:
            query = sa.select(State).where(State.peer_id == peer_id)
            result: typing.Optional[State] = (await conn.execute(query)).fetchone()
            return result

    @staticmethod
    async def set(
        peer_id: int, state: str, payload: typing.Dict[str, typing.Any]
    ) -> typing.Tuple[bool, typing.Optional[Exception]]:
        payload = json.dumps(payload)
        exist = await StateRepository.get(peer_id)
        async with engine.begin() as conn:
            if not exist:
                query = sa.insert(State).values(peer_id=peer_id, state=state, payload=payload)
                try:
                    await conn.execute(query)
                except Exception as exc:
                    await conn.rollback()
                    return False, exc
                else:
                    await conn.commit()
                    return True, None
            else:
                query = (
                    sa.update(State)
                    .values(state=state, payload=payload)
                    .where(State.peer_id == peer_id)
                )
                try:
                    await conn.execute(query)
                except Exception as exc:
                    await conn.rollback()
                    return False, exc
                else:
                    await conn.commit()
                    return True, None

    @staticmethod
    async def delete(peer_id: int) -> typing.Tuple[bool, typing.Optional[Exception]]:
        async with engine.begin() as conn:
            query = sa.delete(State).where(State.peer_id == peer_id)
            try:
                await conn.execute(query)
            except Exception as exc:
                await conn.rollback()
                return False, exc
            else:
                await conn.commit()
                return True, None
