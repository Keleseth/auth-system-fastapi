from typing import Any

from fastapi import HTTPException, status

from auth.abstractions import TUserModel
from auth.domain.entities.user import User
from auth.domain.exceptions import InvalidUserDataError, UserInactiveError
from auth.ports.user_repository import UserRepositoryProtocol
from auth.services.constants import USER_NOT_FOUND_ERROR


async def update_user_role(
    *,
    user_repository: UserRepositoryProtocol,
    user_id: TUserModel,
    role: str
) -> TUserModel | None:
    """
    Обновляет роль пользователя.

    Доступ только для администраторов.
    """
    orm_user_obj = await user_repository.get_user_by_id(user_id)
    if orm_user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=USER_NOT_FOUND_ERROR
        )
    try:
        domain_user: User = user_repository.to_entity(
            orm_user_obj=orm_user_obj
        )
        domain_user.ensure_is_active()
    except (UserInactiveError, InvalidUserDataError) as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    updated_orm_user = await user_repository.update(
        role=role
    )

    return updated_orm_user