from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from email_validator import EmailNotValidError, validate_email

from auth.domain.constants import (
    FIRST_NAME_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH,
    PATRONYMIC_MAX_LENGTH
)
from auth.domain.exceptions import (
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
    email: str
    hashed_password: str
    id: UUID = field(default_factory=uuid4)
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    
    def __post_init__(self) -> None:
        self._validate_email()
        self._validate_incoming_profile_data()

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
        self._validate_incoming_profile_data()

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

    def _validate_email(self) -> None:
        """
        Проверяет валидность формата email.
        """
        try:
            validate_email(self.email)
        except EmailNotValidError:
            raise InvalidUserDataError(INVALID_EMAIL_FORMAT)

    def _validate_incoming_profile_data(self):
        """
        Валидирует входящие данные профиля пользователя(DTO).
        """
        if self.first_name is not None and (
            len(self.first_name) == 0
            or len(self.first_name) > FIRST_NAME_MAX_LENGTH
        ):
            raise InvalidUserDataError(
                INVALID_NAME
            )
        if self.last_name is not None and (
            len(self.last_name) == 0
            or len(self.last_name) > LAST_NAME_MAX_LENGTH
        ):
            raise InvalidUserDataError(
                INVALID_LAST_NAME
            )
        if self.patronymic is not None and (
            len(self.patronymic) == 0
            or len(self.patronymic) > PATRONYMIC_MAX_LENGTH
        ):
            raise InvalidUserDataError(
                INVALID_PATRONYMIC
            )
