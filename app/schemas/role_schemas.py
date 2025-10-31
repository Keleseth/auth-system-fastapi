from pydantic import BaseModel, ConfigDict


class ReadRoleSchema(BaseModel):
    """
    Базовая схема для отдачи данных роли администратору.
    """

    name: str

    model_config = ConfigDict(from_attributes=True)


class UpdateUserRoleSchema(BaseModel):
    """
    Базовая схема для обновления роли пользователя администратором.
    """

    id: int
