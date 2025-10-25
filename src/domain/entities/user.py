from dataclasses import dataclass, field
from datetime import datetime, timezone
from functools import partial
from uuid import UUID, uuid4

from email_validator import EmailNotValidError, validate_email

from src.domain.constants import (
    FIRST_NAME_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH,
    PATRONYMIC_MAX_LENGTH
)
from src.domain.exceptions import (
    INACTIVE_USER,
    INVALID_EMAIL_FORMAT,
    INVALID_NAME,
    INVALID_LAST_NAME,
    INVALID_PATRONYMIC,
    USER_ALREADY_DELETED,
    InvalidUserDataError,
    UserAlreadyDeletedError,
    UserInactiveError
)


@dataclass(slots=True)
class User:
    """
    Корень агрегата пользователя.

    Отвечает за целостность и соблюдение инвариантов, связанных
    с состоянием пользователя, таких как активность, данные профиля
    и аутентификационные данные.

    Является центральной сущностью в домене аутентификации и авторизации.
    """
    id: UUID = field(default_factory=uuid4)
    email: str
    hashed_password: str
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


    @staticmethod
    def create_user(
        email: str,
        hashed_password: str,
        first_name: str | None,
        last_name: str | None,
        patronymic: str | None = None
    ):
        """
        Фабрика для создания нового пользователя.
        """
        User._validate_email(email)
        User._validate_incoming_profile_data(
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic
        )
        return User(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
        )

    def update_profile(
        self,
        first_name: str | None,
        last_name: str | None,
        patronymic: str | None,
    ) -> None:
        """
        Обновляет профиль пользователя, соблюдая инварианты.
        """
        self._ensure_is_active()
        self._ensure_is_not_deleted()
        User._validate_incoming_profile_data(
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic
        )

        self.first_name = first_name
        self.last_name = last_name
        self.patronymic = patronymic

    def soft_delete(self) -> None:
        """
        Выполняет "мягкое" удаление пользователя, соблюдая инварианты.

        Переводит пользователя в деактивированное состояние и устанавливает
        дату удаления.
        """
        self._ensure_is_not_deleted()
        self._ensure_is_active()

        self.is_active = False
        self.deleted_at = datetime.now(timezone.utc)

    def _ensure_is_active(self) -> None:
        """
        Проверяет, что пользователь активен, иначе выбрасывает исключение.

        Предназначается только для операций по изменению
        состояния пользователя. Не предназнаен для аутентификации.
        """
        if not self.is_active:
            raise UserInactiveError(
                INACTIVE_USER
            )

    def _ensure_is_not_deleted(self) -> None:
        """
        Пользователь не удален, дата удаления None.
        """
        if self.deleted_at:
            raise UserAlreadyDeletedError(
                USER_ALREADY_DELETED
            )

    @staticmethod
    def _validate_email(email: str) -> None:
        """
        Проверяет валидность формата email.
        """
        try:
            validate_email(email)
        except EmailNotValidError:
            raise InvalidUserDataError(INVALID_EMAIL_FORMAT)

    @staticmethod
    def _validate_incoming_profile_data(
        first_name: str | None,
        last_name: str | None,
        patronymic: str | None,
    ):
        """
        Валидирует входящие данные профиля пользователя(DTO).
        """
        if first_name is not None and (
            len(first_name) == 0 or len(first_name) > FIRST_NAME_MAX_LENGTH
        ):
            raise InvalidUserDataError(
                INVALID_NAME
            )
        if last_name is not None and (
            len(last_name) == 0 or len(last_name) > LAST_NAME_MAX_LENGTH
        ):
            raise InvalidUserDataError(
                INVALID_LAST_NAME
            )
        if patronymic is not None and (
            len(patronymic) == 0 or len(patronymic) > PATRONYMIC_MAX_LENGTH
        ):
            raise InvalidUserDataError(
                INVALID_PATRONYMIC
            )
