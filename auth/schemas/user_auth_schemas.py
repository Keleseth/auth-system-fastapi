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
    field_validator,
)


class LoginRequestSchema(BaseModel):
    """
    Базовая входная схема для аутентификации пользователя.
    """

    email: EmailStr
    password: str


class UpdateUserSchema(BaseModel):
    """
    Базовая входная схема для обновления профиля пользователя.
    """

    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None


class CreateUserSchema(LoginRequestSchema, UpdateUserSchema):
    """
    Базовая входная схема для регистрации пользователя.
    """

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError(
                'Пароль должен быть не короче 8 символов'
            )
        return value


class ReadUserSchema(UpdateUserSchema):
    """
    Базовая выходная схема для отдачи данных пользователя клиенту.
    """

    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class LoginResponseSchema(BaseModel):
    """
    Базовапя схема передачи токена пользователю.
    """
    access_token: str
    token_type: str


CreateUserSchemaT = TypeVar('CreateUserSchemaT', bound=CreateUserSchema)
ReadUserSchemaT = TypeVar('ReadUserSchemaT', bound=ReadUserSchema)
LoginRequestSchemaT = TypeVar('LoginRequestSchemaT', bound=LoginRequestSchema)
LoginResponseSchemaT = TypeVar(
    'LoginResponseSchemaT',
    bound=LoginResponseSchema
)
UpdateUserSchemaT = TypeVar('UpdateUserSchemaT', bound=UpdateUserSchema)
