import re

from sqlalchemy.orm import DeclarativeBase, declared_attr


class BaseModel(DeclarativeBase):
    """
    Базовый класс для всех моделей проекта(SQLAlchemy).
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Определяет название таблиц всех наследников в формате snake_case.
        """
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
