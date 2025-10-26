"""
Модели:
    RoleMixin - миксин для ролей пользователей.
"""
from sqlalchemy import (
    CheckConstraint,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from auth.domain.constants import (
    ROLE_DESCRIPTION_MAX_LENGTH,
    USER_ROLE_MAX_LENGTH
)


class RoleMixin:
    """
    Миксин для модели Role.
    Предоставляет поля id, name, description.
    Не является готовой моделью, должен быть унаследован вместе с
    декларативной моделью (DeclarativeBase) конечного приложения.
    Связи с другими моделями (например, с пользователями) должны
    быть определены в конечном приложении.
    """
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(USER_ROLE_MAX_LENGTH),
        unique=True,
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        String(ROLE_DESCRIPTION_MAX_LENGTH),
        nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            'char_length(btrim(name)) >= 1',
            name='ck_role_name_minlen'
        ),
    )
