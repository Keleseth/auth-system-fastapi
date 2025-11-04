from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from app.core.constants import ROLE_NOT_FOUND
from app.crud import role_crud
from auth.exceptions.custom_exceptions import RepositoryError


async def update_role_permission_level_use_case(
    role_id: int,
    role_new_permission_level: int,
    session: AsyncSession,
) -> None:
    """
    Обновляет уровень доступа(permission_level) у роли.
    """

    role = await role_crud.get_role(
        role_id=role_id,
        session=session
    )
    if role is None:
        raise HTTPException(
            detail=ROLE_NOT_FOUND.format(role_id=role_id),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    role.permission_level = role_new_permission_level
    await role_crud.change_role_permission_level(
        role=role,
        new_permission_level=role_new_permission_level,
        session=session
    )
    try:
        await role_crud.commit_changes(session=session)
    except RepositoryError as error:
        raise HTTPException(
            detail=str(error),
            status_code=status.HTTP_400_BAD_REQUEST
        ) from error
