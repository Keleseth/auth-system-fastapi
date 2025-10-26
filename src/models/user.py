"""
Модели:
    UserModel - модель пользователей.
"""
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    String,
    text,
    UUID as SQUUID
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.domain.constants import (
    EMAIL_MAX_LENGTH,
    FIRST_NAME_MAX_LENGTH,
    HASHED_PASSWORD_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH,
    PATRONYMIC_MAX_LENGTH
)
from src.models.base import Base
from src.models.role import user_role_association


if TYPE_CHECKING:
    from .role import RoleModel


class UserModel(Base):

    id: Mapped[UUID] = mapped_column(
        SQUUID,
        primary_key=True,
        default=uuid4
    )
    email: Mapped[str] = mapped_column(
        String(EMAIL_MAX_LENGTH),
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(HASHED_PASSWORD_MAX_LENGTH),
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
        server_default=text('true'),
        nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    roles: Mapped[list['RoleModel']] = relationship(
        secondary=user_role_association,
        back_populates='users',
        passive_deletes=True
    )

    __table_args__ = (
        CheckConstraint(
            'first_name IS NULL OR char_length(btrim(first_name)) >= 1',
            name='ck_first_name_min_length'
        ),
        CheckConstraint(
            'last_name IS NULL OR char_length(btrim(last_name)) >= 1',
            name='ck_last_name_min_length'
        ),
        CheckConstraint(
            'patronymic IS NULL OR char_length(btrim(patronymic)) >= 1',
            name='ck_patronymic_min_length'
        )
    )
