from dataclasses import dataclass

from typing import Generic
from auth.schemas.auth import (
    CreateUserSchema,
    CreateUserSchemaT,
    ReadUserSchema,
    ReadUserSchemaT
)


@dataclass(frozen=True, slots=True)
class AuthSchemas(Generic[CreateUserSchemaT, ReadUserSchemaT]):
    """
    Датакласс - контейнер для кастомных и дефолтных схем системы
    аутентификации и авторизации.

    Назначение:
    - Если нужны кастомные схемы, наследуйтесь от базовых схем из аннотации,
    подмените их в экземпляре этого контейнера и передайте в фабрику роутера.
    """

    create: type[CreateUserSchemaT] = CreateUserSchema
    read: type[ReadUserSchemaT] = ReadUserSchema
