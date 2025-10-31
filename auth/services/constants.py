TOKEN_TYPE = 'Bearer '


# --- ошибки --- #
EMAIL_OCCUPIED_ERROR = 'Email уже занят'
USER_NOT_FOUND_ERROR = 'Пользователь не найден'
INVALID_ACCESS_TOKEN_ERROR = 'Неверный токен доступа'
INACTIVE_USER = 'Пользователь неактивен'

# Общая ошибка для любых неудачных попыток аутентификации:
# удаленный или неактивный пользователь, неверный email или пароль...
WRONG_EMAIL_OR_PASSWORD = 'Неверный email или пароль'


# Серверные ошибки
DELETE_USER_ERROR = 'Ошибка при удалении пользователя'
LOGIN_ERROR = 'Ошибка при попытке войти в систему. Попробуйте позже'