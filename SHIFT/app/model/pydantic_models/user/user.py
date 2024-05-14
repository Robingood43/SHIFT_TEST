import datetime

from pydantic import BaseModel, EmailStr


class DecodeToken(BaseModel):
    id: int
    username: EmailStr


class UserLogin(BaseModel):
    username: EmailStr
    password: str


class SalaryDetailsCreate(BaseModel):
    salary: float
    next_raise_date: datetime.date


class Token(BaseModel):
    access_token: str
    token_type: str
