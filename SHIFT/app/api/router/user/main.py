from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from SHIFT.app.controller import create_access_token, check_token
from SHIFT.app.model import SalaryDetailsCreate, Token, DatabaseUserGateway

router = APIRouter()


# Роут для выдачи токена по логину и паролю
@router.post("/login", response_model=Token)
async def login_for_access_token(
        database: Annotated[DatabaseUserGateway, Depends()], form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await database.get_user_by_email_and_password(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or hashed_password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"username": user.username, "id_": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/salary", response_model=SalaryDetailsCreate)
async def get_salary(
        database: Annotated[DatabaseUserGateway, Depends()], token: Annotated[OAuth2PasswordBearer(tokenUrl="login"), Depends()],
) -> SalaryDetailsCreate | HTTPException:
    decode_token = await check_token(database, token)
    salary = await database.get_salary_details(decode_token.id)
    if salary:
        return SalaryDetailsCreate(salary=salary.salary, next_raise_date=salary.next_raise)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Salary not found")
