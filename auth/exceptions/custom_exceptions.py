class AuthBaseError(Exception):
    """
    Базовый класс ошибки системы аутентификации.
    """
    pass


class RepositoryError(AuthBaseError):
    """
    Любая другая ошибка репозитория.
    """
    pass
