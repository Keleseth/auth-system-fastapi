from typing import TYPE_CHECKING

from sqlalchemy import text
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

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

    Связь с ролями определяется здесь.
    """

    is_superuser: Mapped[bool] = mapped_column(
        default=False,
        server_default=text('false'),
        nullable=False
    )
    roles: Mapped[list['RoleModel']] = relationship(
        secondary=user_role_association,
        back_populates='users',
        lazy='selectin'
    )

    def __str__(self) -> str:
        return f'Пользователь: {self.name}'

    def __repr__(self):
        return f'<Пользователь: id={self.id} email={self.email}>'
