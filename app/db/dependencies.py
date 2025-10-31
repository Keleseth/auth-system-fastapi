from typing import Any, AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.user import UserModel
from auth.adapters.sqlalchemy.user_repository import (
    SQLAlchemyUserRepository
)
from auth.ports.user_repository import (
    UserRepositoryProtocol
)



def get_sessionmaker(request: Request) -> sessionmaker:
    """
    Возвращает фабрику сессий SQLAlchemy из состояния приложения.
    Engine хранится в app.state.db_engine из lifespan.
    """
    engine = request.app.state.db_engine
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session(
    _sessionmaker: sessionmaker = Depends(get_sessionmaker),
) -> AsyncGenerator[AsyncSession, Any]:
    async with _sessionmaker() as async_session:
        yield async_session


def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserRepositoryProtocol:
    """
    Склеивает внутри адаптер на протоколе UserRepositoryProtocol(SQLAlchemy)
    с сессией и моделью пользователя.
    """
    return SQLAlchemyUserRepository(
        session=session,
        user_model=UserModel
    )
