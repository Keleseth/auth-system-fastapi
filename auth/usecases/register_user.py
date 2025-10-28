from typing import Any, Dict

from fastapi import HTTPException, status

from auth.abstractions import TUserModel
from auth.domain.entities.user import User
from auth.domain.exceptions import InvalidUserDataError
from auth.exceptions.custom_exceptions import CustomUniqueViolationError
from auth.ports.user_repository import UserRepositoryProtocol
from auth.security.password import DEFAULT_HASHER, PasswordHasher

async def register_user(
    *,
    user_repository: UserRepositoryProtocol,
    hasher: PasswordHasher = DEFAULT_HASHER,
    email: str,
    password: str,
    first_name: str = None,
    last_name: str = None,
    patronymic: str = None,
    **extra_fields: Dict[str, Any],
) -> TUserModel | None:
    user_exists = await user_repository.get_by_email(email)
    if user_exists:
        raise HTTPException(
            detail='Email уже занят',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    hashed_password = hasher.hash(password)

    try:
        user = User(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic
        )
    except InvalidUserDataError as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    user_data = user_repository.map_entity_to_data(
        user,
        **extra_fields
    )
    user = await user_repository.create(
        **user_data        
    )
    try:
        await user_repository.commit()
        return user
    except Exception:
        await user_repository.rollback()
        return None
