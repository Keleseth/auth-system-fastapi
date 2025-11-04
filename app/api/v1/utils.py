from app.core.constants import (
    NO_ROLE_PERMISSION_LEVEL,
    SUPERUSER_PERMISSION_LEVEL,
)
from app.models.user import UserModel


def get_user_max_permission_level(user: UserModel) -> int:
    if user.is_superuser:
        return SUPERUSER_PERMISSION_LEVEL
    if user.roles:
        return max(role.permission_level for role in user.roles)
    return NO_ROLE_PERMISSION_LEVEL
