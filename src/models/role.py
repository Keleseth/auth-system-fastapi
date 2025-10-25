"""
Модели:
    RoleModel - роли пользователей для идентификации доступов.
    user_role_association - связующая между пользователями и ролями.
"""
from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    UUID
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.domain.constants import USER_ROLE_MAX_LENGTH
from src.models.base import Base


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
    users: Mapped[list['UserModel']] = relationship(
        secondary='user_role_association',
        back_populates='roles'
    )


user_role_association = Table(
    'user_role_association',
    Base.metadata,
    Column('user_id', UUID, ForeignKey('user_model.id')),
    Column('role_id', Integer, ForeignKey('role_model.id'))
)
