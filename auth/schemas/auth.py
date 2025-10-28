"""
Базовые Pydantic схемы для аутентификации и управления пользователями.
Если нужны дополнительные поля, унаследуйтесь от этих классов в своём
приложении и передайте свои схемы-наследники в фабрику роутера.
"""
from datetime import datetime
from typing import Any, TypeVar

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class CreateUserSchema(BaseModel):
    """
    Базовая входная схема для регистрации пользователя.
    """

    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None


class ReadUserSchema(BaseModel):
    """
    Базовая выходная схема для отдачи данных пользователя клиенту.
    """

    id: Any
    email: EmailStr
    is_active: bool
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


CreateUserSchemaT = TypeVar('CreateUserSchemaT', bound=CreateUserSchema)
ReadUserSchemaT = TypeVar('ReadUserSchemaT', bound=ReadUserSchema)

