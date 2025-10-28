from typing import Any, AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.user import UserModel
from auth.abstractions import UserModelProtocol
from auth.ports.user_repository import (
    SQLAlchemyUserRepository,
    UserRepositoryProtocol
)


def get_sessionmaker(request: Request) -> sessionmaker:
    # engine хранится в app.state через lifespan
    engine = request.app.state.db_engine
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session(
    _sessionmaker: sessionmaker = Depends(get_sessionmaker),
) -> AsyncGenerator[AsyncSession, Any]:
    async with _sessionmaker() as async_session:
        yield async_session


def get_user_repository(
    user_model: type[UserModelProtocol] = UserModel,
    session: AsyncSession = Depends(get_async_session),
) -> UserRepositoryProtocol:
    """
    Склеивает внутри SQLAlchemyUserRepository 
    с сессией и моделью пользователя.
    """
    return SQLAlchemyUserRepository(
        session=session,
        user_model=user_model
    )
