from fastapi import HTTPException, status

from auth.abstractions import TUserModel
from auth.domain.entities.user import User
from auth.domain.exceptions import UserAlreadyDeletedError, UserInactiveError
from auth.exceptions.custom_exceptions import RepositoryError
from auth.ports.user_repository import UserRepositoryProtocol


async def logout_user(
    *,
    orm_user_obj: TUserModel,
    user_repository: UserRepositoryProtocol,
) -> None:
    """
    Разлогинивает пользователя: инкрементирует token_version
    делая старые токены недействительными.
    """
    domain_user: User = user_repository.to_entity(orm_user_obj=orm_user_obj)
    try:
        domain_user.ensure_is_active()
    except (UserInactiveError, UserAlreadyDeletedError) as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        )
    await user_repository.update_token_version(orm_user_obj)
    try:
        await user_repository.commit()
    except RepositoryError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        ) from error
