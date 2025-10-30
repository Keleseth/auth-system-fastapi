from abc import ABC, abstractmethod
from base64 import b64encode, b64decode
from dataclasses import dataclass
from hmac import compare_digest
import hashlib
import os


class PasswordHasher(ABC):
    """
    Абстрактный класс для бэкенда хеширования паролей.

    Методы:
      - hash(password: str) -> str: возвращает хеш пароля.
      - verify(password: str, hashed: str) -> bool: сверяет пароль с хешем.
    """

    @abstractmethod
    def hash(self, password: str) -> str:  # noqa
        pass

    @abstractmethod
    def verify(self, password: str, hashed: str) -> bool:  # noqa
        pass


@dataclass(frozen=True, slots=True)
class PBKDF2Hasher(PasswordHasher):
    """
    Дефолтный бэкенд хеширования паролей, использующий PBKDF2 с HMAC-SHA256.
    200,000 итераций и соль размером 16 байт.

    Может быть подменен для роутера аутентификации,
    на любой другой, реализующий PasswordHasher.
    """
    iterations: int = 200000
    salt_size: int = 16
    algorithm: str = 'sha256'

    def hash(self, password: str) -> str:
        salt = os.urandom(self.salt_size)
        hashed_string = hashlib.pbkdf2_hmac(
            self.algorithm,
            password.encode('utf-8'),
            salt,
            self.iterations
        )
        return (
            f'pbkdf2${self.iterations}${b64encode(salt).decode("ascii")}'
            f'${b64encode(hashed_string).decode("ascii")}'
        )

    def verify(self, password: str, hashed: str) -> bool:
        try:
            scheme, iter_str, salt_b64, hash_b64 = hashed.split('$')
            if scheme != 'pbkdf2':
                return False
            iterations = int(iter_str)
            salt = b64decode(salt_b64)
            expected = b64decode(hash_b64)
            hashed_string = hashlib.pbkdf2_hmac(
                self.algorithm,
                password.encode('utf-8'),
                salt,
                iterations
            )
            return compare_digest(hashed_string, expected)
        except Exception:
            return False


DEFAULT_HASHER = PBKDF2Hasher()
