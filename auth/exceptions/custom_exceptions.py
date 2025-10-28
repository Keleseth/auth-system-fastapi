class AuthBaseError(Exception):
    """
    Базовый класс ошибки системы аутентификации.
    """
    pass


class CustomUniqueViolationError(AuthBaseError):
    """
    Нарушение уникальности в базе даенных.
    """
    def __init__(
        self,
        detail: str = 'Ошибка уникальности',
        status_code: int = 400,
        field: str | None = None,
        value: str | None = None
    ):
        self.detail = detail
        self.field = field
        self.value = value
        self.status_code = status_code
        super().__init__(detail)


class RepositoryError(AuthBaseError):
    """
    Любая другая ошибка репозитория/хранилища.
    """
    pass
