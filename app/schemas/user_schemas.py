from datetime import datetime

from pydantic import ConfigDict

from auth.schemas.user_auth_schemas import (
    ReadUserSchema,
)
from app.schemas.role_schemas import ReadRoleSchema


class ReadUserSchemaAdmin(ReadUserSchema):
    """
    Расширенная схема чтения пользователя для администраторов.
    """

    last_name: str | None = None
    first_name: str | None = None
    patronymic: str | None = None
    is_active: bool
    created_at: datetime | None = None
    update_at: datetime | None = None
    deleted_at: datetime | None = None
    roles: list[ReadRoleSchema]

    model_config = ConfigDict(from_attributes=True)
