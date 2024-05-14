from typing import Optional

import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from SHIFT.app.model import User, DatabaseUserGateway, SalaryDetails


def check_password(password: str, hashed_password: str) -> bool:
    stored_hash_bytes = hashed_password.encode()
    hashed_input = bcrypt.hashpw(password.encode(), stored_hash_bytes)
    return hashed_input == stored_hash_bytes


def get_password_hash(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password.decode()


class SqlaUserGateway(DatabaseUserGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id_and_email(self, id_, username) -> Optional[User]:
        user = await self.session.scalars(select(User).filter_by(id=id_, username=username))
        return user.first()

    async def get_user_by_email_and_password(self, username: str, password: str) -> Optional[User]:
        user = await self.session.scalars(select(User).filter_by(username=username))
        user = user.first()
        if user is None:
            return None
        if check_password(password, user.hashed_password):
            return user
        return None

    async def get_salary_details(self, id_: int) -> Optional[SalaryDetails]:
        salary_details = await self.session.scalars(select(SalaryDetails).filter_by(id=id_))
        return salary_details.first()
