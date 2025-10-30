from fastapi import HTTPException, status

from auth.domain.entities.user import User
from auth.domain.exceptions import InvalidUserDataError, UserAlreadyDeletedError, UserInactiveError
from auth.ports.user_repository import UserRepositoryProtocol
from auth.services.constants import WRONG_EMAIL_OR_PASSWORD
from auth.services.security.token_service import TokenService
from auth.services.security.password import (
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
            detail=WRONG_EMAIL_OR_PASSWORD,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    try:
        domain_user = user_repository.to_entity(orm_user_obj)
        domain_user.verify_user_can_authenticate()
    except InvalidUserDataError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )
    except (UserInactiveError, UserAlreadyDeletedError) as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        )
    if not hasher.verify(password, domain_user.hashed_password):
        raise HTTPException(
            detail=WRONG_EMAIL_OR_PASSWORD,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    token = token_service.provide_access_token(
        sub=str(domain_user.id),
        token_version=int(orm_user_obj.token_version)
    )
    return token
