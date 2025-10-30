from abc import ABC
from datetime import datetime
from typing import TypeVar
from uuid import UUID


class UserModelTypeHint:
    """
    Контракт для ORM-модели пользователя.

    Любая модель пользователя должна соответствовать этому контракту.
    Наследование не требуется, достаточно совместимости по атрибутам.
    """

    id: UUID
    email: str
    hashed_password: str
    is_active: bool
    token_version: int = 0
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

TUserModel = TypeVar('TUserModel', bound=UserModelTypeHint)