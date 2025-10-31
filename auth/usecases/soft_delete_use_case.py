
from fastapi import HTTPException, status

from auth.abstractions import TUserModel
from auth.domain.entities.user import User
from auth.domain.exceptions import UserAlreadyDeletedError, UserInactiveError
from auth.exceptions.custom_exceptions import RepositoryError
from auth.ports.user_repository import UserRepositoryProtocol



async def soft_delete_usecase(
    *,
    orm_user_obj: TUserModel,
    user_repository: UserRepositoryProtocol
) -> None:
    """
    Мягко удаляет пользователя (soft-delete),
    помечает неактивным - is_active и проставляет дату удаления - deleted_at.
    """
    domain_user: User = user_repository.to_entity(orm_user_obj)
    try:
        domain_user.soft_delete()
    except (UserAlreadyDeletedError, UserInactiveError) as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error)
        )
    await user_repository.soft_delete(
        user=orm_user_obj,
        active_status=domain_user.is_active,
        deleted_at=domain_user.deleted_at
    )
    try:
        await user_repository.commit()
    except RepositoryError as error:
        await user_repository.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        ) from error
