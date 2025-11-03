from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from auth.sqlalchemy_mixins import (
    RoleMixin,
    TimeStampMixin,
)
from .associations import user_role_association
from .base import BaseModel

if TYPE_CHECKING:
    from .user import UserModel


class RoleModel(BaseModel, RoleMixin, TimeStampMixin):
    """
    Модель роли пользователя.

    Связь с пользователями определяется здесь.
    """
    users: Mapped[list['UserModel']] = relationship(
        secondary=user_role_association,
        back_populates='roles',
        lazy='selectin'
    )

    def __str__(self) -> str:
        return f'Роль: {self.name}'

    def __repr__(self):
        return f'<Роль: id={self.id} название={self.name}>'