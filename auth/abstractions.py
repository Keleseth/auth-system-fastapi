from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID


class AbstractUser(ABC):
    """
    Абстрактный класс - контракт, определяющий, какие свойства
    должна предоставлять модель пользователя для корректной работы
    библиотеки аутентификации.
    """

    @property
    @abstractmethod
    def id(self) -> UUID:
        """Уникальный идентификатор пользователя."""
        raise NotImplementedError

    @property
    @abstractmethod
    def email(self) -> str:
        """Email пользователя."""
        raise NotImplementedError

    @property
    @abstractmethod
    def hashed_password(self) -> str:
        """Хэшированный пароль пользователя."""
        raise NotImplementedError

    @property
    @abstractmethod
    def is_active(self) -> bool:
        """Активен ли пользователь."""
        raise NotImplementedError

    @property
    @abstractmethod
    def created_at(self) -> datetime:
        """Время создания пользователя."""
        raise NotImplementedError

    @property
    @abstractmethod
    def updated_at(self) -> datetime:
        """Время последнего обновления пользователя."""
        raise NotImplementedError
