# Ошибки App приложения
USER_NOT_FOUND = 'Пользователь с id: {user_id} не найден'
ROLE_NOT_FOUND = 'Роль с id: {role_id} не найдена'
APPLY_ROLE_TO_USER_ERROR = (
    'Ошибка при добавлении роли c {role_id} пользователю {user_id}'
)
CANT_PROMOTE_HIGHER_OR_EQUAL_ROLE = (
    'Нельзя назначить роль с уровнем прав выше или равным вашему'
)
CANT_REMOVE_HIGHER_OR_EQUAL_ROLE = (
    'Нельзя снять роль с уровнем прав выше или равным вашему'
)
LIMITED_ACCESS = 'Недостаточно прав'
OBJECT_NOT_FOUND = 'Объект не найден'

# Уровни доступа
SUPERUSER_PERMISSION_LEVEL = 100000
ADMIN_PERMISSION_LEVEL = 100
LEAD_MODERATOR = 75
USER_PERMISSION_LEVEL = 10
NO_ROLE_PERMISSION_LEVEL = 0
