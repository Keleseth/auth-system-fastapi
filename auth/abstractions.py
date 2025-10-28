from abc import ABC
from datetime import datetime
from typing import TypeVar
from uuid import UUID


class AbstractUserModel:
    """
    Контракт для ORM-модели пользователя.

    Любая модель пользователя должна соответствовать этому протоколу.
    Наследование не требуется, достаточно совместимости по атрибутам.
    """

    id: UUID
    email: str
    hashed_password: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

TUserModel = TypeVar('TUserModel', bound=AbstractUserModel)