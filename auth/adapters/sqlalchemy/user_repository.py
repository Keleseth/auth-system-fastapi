"""
Адаптер (SQLAlchemyUserRepository) - конкретная реализация на SQLAlchemy,
которая замыкает в себе AsyncSession и ORM-модель пользователя.

Адаптер пользователей создаётся в зависимостях приложения
и передаётся в эндпоинт через Depends.
"""
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.abstractions import TUserModel
from auth.domain.entities.user import User
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
        - Все методы репозитория являются асинхронными для единообразия.
    """

    def __init__(
        self,
        session: AsyncSession,
        user_model: type[TUserModel]
    ) -> None:
        self._session = session
        self._user_model = user_model

    async def get_user_by_id(self, user_id: UUID) -> TUserModel | None:
        """
        Получает пользователя по ID.
        """
        result = await self._session.execute(
            select(self._user_model).where(self._user_model.id==user_id)
        )
        return result.scalar_one_or_none()

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


    async def soft_delete(
        self,
        user: TUserModel,
        active_status: bool = False,
        deleted_at: datetime | None = None,
    ) -> None:
        user.is_active = active_status
        user.deleted_at = deleted_at or datetime.now(timezone.utc)
        self._session.add(user)

    async def update_token_version(self, user: TUserModel) -> None:
        user.token_version += 1
        self._session.add(user)

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except Exception as error:
            await self._session.rollback()
            raise RepositoryError(
                'Ошибка завершения транзакции'
            ) from error

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

    def to_entity(self, orm_user_obj: Any) -> User:
        """
        Маппит ORM-модель пользователя в доменную сущность.
        Ожидает, что orm_obj имеет атрибуты, совместимые с доменной сущностью.
        """
        return User(
            id=orm_user_obj.id,
            email=orm_user_obj.email,
            hashed_password=orm_user_obj.hashed_password,
            first_name=orm_user_obj.first_name,
            last_name=orm_user_obj.last_name,
            patronymic=orm_user_obj.patronymic,
            is_active=orm_user_obj.is_active,
            created_at=orm_user_obj.created_at,
            updated_at=orm_user_obj.updated_at,
            deleted_at=orm_user_obj.deleted_at
        )

    def get_session(self) -> AsyncSession:
        """
        Возвращает рабочую сессию.

        Метод нужен для передачи сессии в другие репозитории.
        """
        return self._session
