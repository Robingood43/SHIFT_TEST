from abc import ABC, abstractmethod
from typing import Optional

from SHIFT.app.model.database.schemas.schemas import User, SalaryDetails


class DatabaseUserGateway(ABC):
    @abstractmethod
    async def get_user_by_id_and_email(self, id_, username) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email_and_password(self, username: str, password: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_salary_details(self, id_: int) -> Optional[SalaryDetails]:
        raise NotImplementedError
