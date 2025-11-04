from pydantic import BaseModel, ConfigDict, Field


class ReadRoleSchema(BaseModel):
    """
    Базовая схема для отдачи данных роли администратору.
    """

    name: str

    model_config = ConfigDict(from_attributes=True)


class UpdateRoleSchema(BaseModel):
    """
    Базовая схема для обновления роли администратором.
    """

    permission_level: int = Field(ge=0, le=100)
