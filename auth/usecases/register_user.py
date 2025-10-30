from typing import Any, Dict

from fastapi import HTTPException, status

from auth.abstractions import TUserModel
from auth.domain.entities.user import User
from auth.domain.exceptions import InvalidUserDataError
from auth.ports.user_repository import UserRepositoryProtocol
from auth.services.constants import EMAIL_OCCUPIED_ERROR
from auth.services.security.password import DEFAULT_HASHER, PasswordHasher

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
    """
    Регистрирует нового пользователя в системе.
    """
    email_occupied = await user_repository.check_email_occupied(email)
    if email_occupied:
        raise HTTPException(
            detail=EMAIL_OCCUPIED_ERROR,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    hashed_password = hasher.hash(password)

    try:
        domain_user: User = User(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic
        )
    except InvalidUserDataError as error:
        raise HTTPException(
            detail=str(error),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    user_data = user_repository.map_entity_to_data(
        domain_user,
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
