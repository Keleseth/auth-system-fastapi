"""
Порт репозитория пользователя.

Порт (UserRepositoryProtocol) - контракт для use-case
со всеми нужными операциями.
"""
from typing import Protocol, Any
from uuid import UUID

from auth.abstractions import TUserModel
from auth.domain.entities.user import User


class UserRepositoryProtocol(Protocol[TUserModel]):
    """
    Контракт репозитория пользователя для use-case.

    Содержит только методы для доступа к данным.
    """

    async def get_user_by_id(self, user_id: UUID) -> TUserModel | None:
        """
        Получает пользователя по ID.
        """
        pass

    async def get_by_email(self, email: str) -> TUserModel | None:
        """
        Получает пользователя по email.
        """
        pass

    async def check_email_occupied(self, email: str) -> bool:
        """
        Проверяет, занята ли почта в базе данных.
        """
        pass

    async def add(self, user: TUserModel) -> None:
        pass

    async def create(self, **fields: Any) -> TUserModel:
        """
        Создает нового пользователя в базе данных.
        """
        pass

    async def update(
            self,
            user: TUserModel,
            **fields: Any
    ) -> TUserModel:
        """
        Обновляет пользователя в базе данных.
        """
        pass

    async def soft_delete(self, user: TUserModel) -> None:
        """
        Удаляет пользователя из базы данных.
        """
        pass

    async def update_token_version(self, user: TUserModel) -> None:
        """
        Обновляет версию токена пользователя.
        """
        pass

    async def commit(self) -> None:
        """
        Коммитит текущую транзакцию.
        """
        pass

    async def rollback(self) -> None:
        """
        Откатывает текущую транзакцию.
        """
        pass

    def map_entity_to_data(self, entity: Any, **extra_fields: Any) -> Any:
        """
        Маппит доменную сущность пользователя в словарь данных + extra_fields.
        """
        pass

    def to_entity(self, orm_user_obj: Any) -> User:
        """
        TODO продумать реализацию.
        """
        pass
