from pydantic import BaseModel, ConfigDict


class ReadRoleSchema(BaseModel):
    """
    Базовая выходная схема для отдачи данных роли клиенту.
    """

    name: str

    model_config = ConfigDict(from_attributes=True)