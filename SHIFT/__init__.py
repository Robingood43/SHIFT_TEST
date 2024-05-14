import datetime
from functools import partial

from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from SHIFT.app.api import init_routers
from SHIFT.app.controller import get_db, new_gateway
from SHIFT.app.model import Base, DatabaseUserGateway, User, SalaryDetails
from SHIFT.config import config


def start_app():
    app = FastAPI()

    engine = create_async_engine(config.url_asyncpg, echo=True)
    session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @app.on_event("startup")
    async def startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with session_maker() as session:
            # Создаем двух тестовых пользователей
            user1 = session.scalar(select(User.id).filter_by(username="user@example.com"))
            user2 = session.scalar(select(User.id).filter_by(username="user2@example.com"))
            if user1 is None and user2 is None:
                session.add_all(
                    [
                        User(
                            username="user@example.com",
                            hashed_password="$2b$12$nhEYfC7pRyS.KGZezH7htO5XAj1pg8k/sgJGdYcY6boH2SH1nn4y2"
                        ),
                        User(
                            username="user2@example.com",
                            hashed_password="$2b$12$nhEYfC7pRyS.KGZezH7htO5XAj1pg8k/sgJGdYcY6boH2SH1nn4y2"
                        ),
                        SalaryDetails(
                            id=1,
                            salary=20000.00,
                            next_raise=datetime.datetime.now().date() + datetime.timedelta(days=10),
                        ),
                        SalaryDetails(
                            id=2,
                            salary=30000.00,
                            next_raise=datetime.datetime.now().date() + datetime.timedelta(days=20),
                        )
                    ]
                )
                await session.commit()


    app.dependency_overrides[AsyncSession] = partial(get_db, session_maker)
    app.dependency_overrides[DatabaseUserGateway] = new_gateway
    init_routers(app)
    return app
