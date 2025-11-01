from typing import Any

from fastapi import HTTPException, status

from auth.abstractions import TUserModel
from auth.domain.entities.user import User
from auth.domain.exceptions import (
    InvalidUserDataError,
    UserInactiveError,
    UserAlreadyDeletedError,
)
from auth.exceptions.custom_exceptions import RepositoryError
from auth.ports.user_repository import UserRepositoryProtocol


async def update_user_profile(
    *,
    user_repository: UserRepositoryProtocol,
    orm_user_obj: TUserModel,
    **fields: Any
) -> TUserModel | None:
    """
    Обновляет профиль пользователя:
      -first_name
      -last_name
      -patronymic

    Проверяет валидность данных и статус пользователя пользователя:
      - is_active
      - deleted_at.
    """

    domain_user: User = user_repository.to_entity(
        orm_user_obj=orm_user_obj
    )
    new_first_name = fields.get('first_name', domain_user.first_name)
    new_last_name = fields.get('last_name', domain_user.last_name)
    new_patronymic = fields.get('patronymic', domain_user.patronymic)

    try:
        domain_user.update_profile(
            first_name=new_first_name,
            last_name=new_last_name,
            patronymic=new_patronymic,
        )
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

    updated_user = await user_repository.update(orm_user_obj, **fields)
    try:
        await user_repository.commit()
        return updated_user
    except RepositoryError as error:
        await user_repository.rollback()
        raise HTTPException(
            detail=str(error),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from error
