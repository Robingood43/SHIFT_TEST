from typing import Iterable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from SHIFT.app.controller.controller import Stub
from SHIFT.app.controller.crud.user.user import SqlaUserGateway

__all__ = ["get_db", "new_gateway"]
def new_gateway(session: AsyncSession = Depends(Stub(AsyncSession))):
    yield SqlaUserGateway(session)


async def get_db(session_maker) -> Iterable[AsyncSession]:
    async with session_maker() as session:
        yield session
