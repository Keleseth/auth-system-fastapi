from datetime import datetime
from typing import Protocol
from uuid import UUID


class UserModelProtocol(Protocol):
    """
    Абстрактный класс - контракт, определяющий, какие свойства
    должна предоставлять модель пользователя для корректной работы
    библиотеки аутентификации.
    """

    @property
    def id(self) -> UUID:
        """Уникальный идентификатор пользователя."""
        raise NotImplementedError

    @property
    def email(self) -> str:
        """Email пользователя."""
        raise NotImplementedError

    @property
    def hashed_password(self) -> str:
        """Хэшированный пароль пользователя."""
        raise NotImplementedError

    @property
    def is_active(self) -> bool:
        """Активен ли пользователь."""
        raise NotImplementedError

    @property
    def created_at(self) -> datetime:
        """Время создания пользователя."""
        raise NotImplementedError

    @property
    def updated_at(self) -> datetime:
        """Время последнего обновления пользователя."""
        raise NotImplementedError
