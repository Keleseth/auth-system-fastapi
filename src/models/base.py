from datetime import datetime
import re

from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """
    Базовая модель SQLAlchemy с общими полями и функциональностью.
    """
    __abstract__ = True
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Определяет название таблиц всех наследников в формате snake_case.
        """
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
