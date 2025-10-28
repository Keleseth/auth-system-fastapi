"""
Порт репозитория пользователя.

Порт (UserRepositoryProtocol) - контракт для use-case
со всеми нужными операциями.
"""
from typing import Protocol, Any

from auth.abstractions import TUserModel


class UserRepositoryProtocol(Protocol[TUserModel]):
    """
    Контракт репозитория пользователя для use-case.

    Содержит только методы для доступа к данным.
    """

    async def get_by_email(self, email: str) -> TUserModel | None:
        pass

    async def add(self, user: TUserModel) -> None:
        pass

    async def create(self, **fields: Any) -> TUserModel:
        pass

    async def update(
            self,
            user: TUserModel,
            **fields: Any
    ) -> TUserModel:
        pass

    async def delete(self, user: TUserModel) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass

    def map_entity_to_data(self, entity: Any, **extra_fields: Any) -> Any:
        """
        Маппит доменную сущность пользователя в словарь данных + extra_fields.
        """
        pass

    def to_entity(self, orm_obj: Any) -> Any:
        """
        TODO думаю над реализацией
        """
        pass
