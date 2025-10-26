INVALID_EMAIL_FORMAT = 'Невалидный формат email'
INVALID_NAME = 'Невалидное имя'
INVALID_LAST_NAME = 'Невалидная фамилия'
INVALID_PATRONYMIC = 'Невалидное отчество'
INVALID_PASSWORD = 'Невалидный пароль'
INACTIVE_USER = 'Пользователь не активен'
USER_ALREADY_DELETED = 'Пользователь уже удален'


class DomainException(Exception):
    """
    Базовый класс исключений для доменного слоя.
    """

    @property
    def message(self) -> str:
        return self.args[0]


class UserInactiveError(DomainException):
    """
    Ошибка использования функционала активного пользователя не активным.
    """
    pass


class UserAlreadyDeletedError(DomainException):
    """
    Ошибка при попытке удаления уже удаленного пользователя.
    """
    pass


class InvalidUserDataError(DomainException):
    """
    Ошибка невалидных данных профиля пользователя:
        - Имя
        - Фамилия
        - Отчество
        - email
        - пароль
    """
    pass