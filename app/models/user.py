from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from auth.sqlalchemy_mixins import (
    UserMixin,
    TimeStampMixin,
)
from .associations import user_role_association
from .base import BaseModel

if TYPE_CHECKING:
    from .role import RoleModel


class UserModel(BaseModel, UserMixin, TimeStampMixin):
    """
    Модель пользователя.
    Наследуется от Base, UserMixin и TimeStampMixin.
    Связь с ролями определяется здесь.
    """

    roles: Mapped[list['RoleModel']] = relationship(
        secondary=user_role_association,
        back_populates='users',
        lazy='selectin'
    )
