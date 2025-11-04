from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth.sqlalchemy_mixins import (
    RoleMixin,
    TimeStampMixin,
)
from app.models.associations import user_role_association
from app.models.base import BaseModel

if TYPE_CHECKING:
    from .user import UserModel


class RoleModel(BaseModel, RoleMixin, TimeStampMixin):
    """
    Модель роли пользователя.

    Связь с пользователями определяется здесь.
    """

    permission_level: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default=text('0'),
        nullable=False
    )
    users: Mapped[list['UserModel']] = relationship(
        secondary=user_role_association,
        back_populates='roles',
        lazy='selectin'
    )

    __table_args__ = (
        CheckConstraint(
            'char_length(btrim(name)) >= 1',
            name='ck_role_name_minlen'
        ),
        CheckConstraint(
            'permission_level >= 0 AND permission_level <= 100',
            name='ck_role_permission_level_min_max'
        ),
    )

    def __str__(self) -> str:
        return f'Роль: {self.name}'

    def __repr__(self):
        return f'<Роль: id={self.id} название={self.name}>'
