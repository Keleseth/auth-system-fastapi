from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict

from app.schemas.role_schemas import ReadRoleSchema
from auth.schemas.user_auth_schemas import (
    ReadUserSchema,
)


class ReadUserSchemaAdmin(ReadUserSchema):
    """
    Расширенная схема чтения пользователя для администраторов.
    """
    id: UUID
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    roles: list[ReadRoleSchema]

    model_config = ConfigDict(from_attributes=True)
