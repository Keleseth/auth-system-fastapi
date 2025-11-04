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

# API префиксы эндпоинтов для тестов и боевого сервера

AUTH_PREFIX = '/auth'
REGISTER_PREFIX = '/register'
LOGIN_PREFIX = '/login'
LOGOUT_PREFIX = '/logout'
UPDATE_PROFILE_PREFIX = '/users/me'
SOFT_DELETE_USER_PREFIX = '/users/me'
