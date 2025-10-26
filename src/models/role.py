"""
Модели:
    RoleModel - роли пользователей для идентификации доступов.
    user_role_association - связующая между пользователями и ролями.
"""
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    UUID as SQUUID
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from auth.domain.constants import ROLE_DESCRIPTION_MAX_LENGTH, USER_ROLE_MAX_LENGTH
from auth.sqlalchemy_mixins.timestamp_mixin import Base


if TYPE_CHECKING:
    from .user import UserModel


class RoleModel(Base):

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
    users: Mapped[list['UserModel']] = relationship(
        secondary='user_role_association',
        back_populates='roles',
        passive_deletes=True
    )

    __table_args__ = (
        CheckConstraint(
            'char_length(btrim(name)) >= 1',
            name='ck_role_name_minlen'
        ),
    )


user_role_association = Table(
    'user_role_association',
    Base.metadata,
    Column(
        'user_id',
        SQUUID,
        ForeignKey('user_model.id', ondelete='CASCADE'),
        primary_key=True
    ),
    Column(
        'role_id',
        Integer,
        ForeignKey('role_model.id', ondelete='CASCADE'),
        primary_key=True
    )
)
