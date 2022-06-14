import typing

from vkbottle import ABCStateDispenser, BaseStateGroup, StatePeer

from src.database.repositories import StateRepository
from src.modules import json

__all__ = ("StateDispenser",)


class StateDispenser(ABCStateDispenser):
    def __init__(self, *args, **kwargs):
        pass

    async def get(self, peer_id: int) -> typing.Optional[StatePeer]:
        state = await StateRepository.get(peer_id)
        if state is None:
            return None
        try:
            payload = json.loads(state.payload)
        except json.JSONDecodeError:
            payload = state.payload or {}
        return StatePeer(peer_id=peer_id, state=state.state, payload=payload)

    async def set(self, peer_id: int, state: BaseStateGroup, **payload):
        await StateRepository.set(peer_id, state.name, payload)

    async def delete(self, peer_id: int):
        await StateRepository.delete(peer_id)
