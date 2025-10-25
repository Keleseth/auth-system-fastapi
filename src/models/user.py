"""
Модели:
    UserModel - модель пользователей.
"""
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import String, DateTime
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.domain.constants import (
    FIRST_NAME_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH,
    PATRONYMIC_MAX_LENGTH
)
from src.models.base import Base
from src.models.role import user_role_association


if TYPE_CHECKING:
    from .role import RoleModel


class UserModel(Base):

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )
    email: Mapped[str] = mapped_column(
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        nullable=False
    )
    first_name: Mapped[str | None] = mapped_column(
        String(FIRST_NAME_MAX_LENGTH)
    )
    last_name: Mapped[str | None] = mapped_column(
        String(LAST_NAME_MAX_LENGTH)
    )
    patronymic: Mapped[str | None] = mapped_column(
        String(PATRONYMIC_MAX_LENGTH)
    )
    is_active: Mapped[bool] = mapped_column(
        server_default='true',
        nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    roles: Mapped[list['RoleModel']] = relationship(
        secondary=user_role_association,
        back_populates='users'
    )
