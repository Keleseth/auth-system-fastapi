"""
Адаптер (SQLAlchemyUserRepository) - конкретная реализация на SQLAlchemy,
которая замыкает в себе AsyncSession и ORM-модель пользователя.

Адаптер пользователей создаётся в зависимостях приложения
и передаётся в эндпоинт через Depends.
"""
from typing import Any
from dataclasses import asdict

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.abstractions import TUserModel
from auth.exceptions.custom_exceptions import RepositoryError
from auth.ports.user_repository import UserRepositoryProtocol


class SQLAlchemyUserRepository(UserRepositoryProtocol):
    """
    Адаптер репозитория пользователя.

    Замыкает внутри:
        - session: AsyncSession
        - user_model: ORM-класс пользователя (по абстракции TUserModel).

    Примечания:
        - Сессия закрепляется за объектом репозитория при инициализации в Depends.
    """

    def __init__(self, session: AsyncSession, user_model: type[TUserModel]) -> None:
        self._session = session
        self._user_model = user_model

    async def get_by_email(self, email: str) -> TUserModel | None:
        email = email.lower().strip()
        result = await self._session.execute(
            select(self._user_model).where(self._user_model.email==email)
        )
        return result.scalar_one_or_none()

    async def check_email_occupied(self, email: str) -> bool:
        """
        Проверяет, занята ли почта в базе данных.
        """
        email = email.lower().strip()
        result = await self._session.execute(
            select(
                exists().where(self._user_model.email==email)
            )
        )
        return bool(result.scalar())

    async def add(self, user: TUserModel) -> None:
        self._session.add(user)

    async def create(self, **fields: Any) -> TUserModel:
        """
        Создаёт ORM-экземпляр пользователя и помещает его в сессию без коммита.

        Минимально ожидаемые поля: email, hashed_password.
        """
        user = self._user_model(**fields)
        self._session.add(user)
        return user

    async def update(self, user: TUserModel, **fields: Any) -> TUserModel:
        for key, value in fields.items():
            setattr(user, key, value)
        self._session.add(user)
        return user

    async def delete(self, user: TUserModel) -> None:
        await self._session.delete(user)

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise RepositoryError(
                'Ошибка завершения транзакции'
            ) from e

    async def rollback(self) -> None:
        await self._session.rollback()

    def map_entity_to_data(
        self,
        entity: Any,
        **extra_fields: Any
    ) -> dict:
        """
        Маппит доменную сущность пользователя в ORM-модель.
        Ожидает, что entity имеет атрибуты, совместимые с ORM-моделью.
        """
        data = asdict(entity)
        if extra_fields:
            data.update(extra_fields)
        return data

    def to_entity(self, orm_obj: Any) -> Any:
        """
        Маппит ORM-модель пользователя в доменную сущность.
        Ожидает, что orm_obj имеет атрибуты, совместимые с доменной сущностью.
        """
        # Здесь можно использовать dataclass/entity конструктор, если есть
        # Например: return UserEntity(**orm_obj.__dict__)
        return orm_obj
