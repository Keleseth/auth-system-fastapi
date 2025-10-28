from typing import Any, Dict

from auth.abstractions import UserModelProtocol
from auth.ports.user_repository import UserRepositoryProtocol
from auth.security.password import DEFAULT_HASHER, PasswordHasher

async def register_user(
    *,
    user_repository: UserRepositoryProtocol,
    hasher: PasswordHasher = DEFAULT_HASHER,
    email: str,
    password: str,
    **extra_fields: Dict[str, Any],
) -> UserModelProtocol | None:
    pass