from typing import Any

from auth.abstractions import UserModelProtocol
from auth.ports.user_repository import UserRepositoryProtocol


async def update_user_profile(
    *,
    user_repository: UserRepositoryProtocol,
    **extra_fields: Any,
) -> UserModelProtocol:
    pass