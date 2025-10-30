from fastapi import HTTPException, status

from auth.domain.entities.user import User
from auth.ports.user_repository import UserRepositoryProtocol
from auth.security.token_service import TokenService
from auth.security.password import (
    DEFAULT_HASHER,
    PasswordHasher
)


async def authenticate_user(
    *,
    user_repository: UserRepositoryProtocol,
    token_service: TokenService,
    hasher: PasswordHasher = DEFAULT_HASHER,
    email: str,
    password: str,
) -> str:
    orm_user_obj = await user_repository.get_by_email(email)
    if orm_user_obj is None:
        raise HTTPException(
            detail='Неверный email или пароль.',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    user = user_repository.to_entity(orm_user_obj)
    user.verify_user_can_authenticate()
    if not hasher.verify(password, user.hashed_password):
        raise HTTPException(
            detail='Неверный email или пароль.',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    token = token_service.provide_access_token(
        sub=str(user.id)
    )
    return token