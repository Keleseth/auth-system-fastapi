from typing import Any

from auth.abstractions import TUserModel
from auth.ports.user_repository import UserRepositoryProtocol


async def update_user_profile(
    *,
    user_repository: UserRepositoryProtocol,
    **extra_fields: Any,
) -> TUserModel:
    pass