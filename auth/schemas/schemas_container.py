from dataclasses import dataclass

from typing import Generic
from auth.schemas.user_auth_schemas import (
    CreateUserSchema,
    CreateUserSchemaT,
    LoginRequestSchema,
    LoginRequestSchemaT,
    ReadUserSchema,
    ReadUserSchemaT,
    LoginResponseSchema,
    LoginResponseSchemaT,
    UpdateUserSchema,
    UpdateUserSchemaT,
    UpdateUserRoleSchema,
    UpdateUserRoleSchemaT,
    ReadUserSchemaAdmin,
    ReadUserSchemaAdminT,
)


@dataclass(frozen=True, slots=True)
class AuthSchemas(Generic[
    CreateUserSchemaT,
    ReadUserSchemaT,
    LoginRequestSchemaT,
    LoginResponseSchemaT,
    UpdateUserSchemaT,
    UpdateUserRoleSchemaT,
    ReadUserSchemaAdminT,
]):
    """
    Датакласс - контейнер для кастомных и дефолтных схем системы
    аутентификации и авторизации.

    Назначение:
    - Если нужны кастомные схемы, наследуйтесь от базовых схем из аннотации,
    подмените их в экземпляре этого контейнера и передайте в фабрику роутера.
    """

    create: type[CreateUserSchemaT] = CreateUserSchema
    read: type[ReadUserSchemaT] = ReadUserSchema
    update: type[UpdateUserSchemaT] = UpdateUserSchema
    login_request: type[LoginRequestSchemaT] = LoginRequestSchema
    login_response: type[LoginResponseSchemaT] = LoginResponseSchema
    update_role: type[UpdateUserRoleSchemaT] = UpdateUserRoleSchema
    read_user_admin: type[ReadUserSchemaAdminT] = ReadUserSchemaAdmin