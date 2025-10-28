"""
Порт и дефолтный адаптер репозитория пользователя.

Порт (UserRepositoryProtocol) - контракт для use-case
со всеми нужными операциями.
Адаптер (SQLAlchemyUserRepository) - конкретная реализация на SQLAlchemy,
которая замыкает в себе AsyncSession и ORM-модель пользователя.

Адаптер пользователей создаётся в зависимостях приложения
и передаётся в эндпоинт через Depends.
"""

from __future__ import annotations

from typing import Protocol, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.abstractions import UserModelProtocol


class UserRepositoryProtocol(Protocol):
    """
    Контракт репозитория пользователя для use-case.

    Содержит только методы для доступа к данным.
    """

    async def get_by_email(self, email: str) -> UserModelProtocol | None:
        pass

    async def add(self, user: UserModelProtocol) -> None:
        pass

    async def create(self, **fields: Any) -> UserModelProtocol:
        pass

    async def update(
            self,
            user: UserModelProtocol,
            **fields: Any
    ) -> UserModelProtocol:
        pass

    async def delete(self, user: UserModelProtocol) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass


class SQLAlchemyUserRepository(UserRepositoryProtocol):
    """
    Адаптер репозитория пользователя.

    Замыкает внутри:
        - session: AsyncSession
        - user_model: ORM-класс пользователя (по протоколу UserModelProtocol).

    Примечания:
        - Сессия закрепляется за объектом репозитория при инициализации в Depends.
    """

    def __init__(self, session: AsyncSession, user_model: type[UserModelProtocol]) -> None:
        self._session = session
        self._user_model = user_model

    async def get_by_email(self, email: str) -> UserModelProtocol | None:
        result = await self._session.execute(
            select(self._user_model).where(self._user_model.email == email)
        )
        return result.scalar_one_or_none()

    async def add(self, user: UserModelProtocol) -> None:
        self._session.add(user)

    async def create(self, **fields: Any) -> UserModelProtocol:
        """
        Создаёт ORM-экземпляр пользователя и помещает его в сессию без коммита.

        Минимально ожидаемые поля: email, hashed_password.
        """
        obj = self._user_model(**fields)
        self._session.add(obj)
        return obj

    async def update(self, user: UserModelProtocol, **fields: Any) -> UserModelProtocol:
        for key, value in fields.items():
            setattr(user, key, value)
        self._session.add(user)
        return user

    async def delete(self, user: UserModelProtocol) -> None:
        await self._session.delete(user)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
