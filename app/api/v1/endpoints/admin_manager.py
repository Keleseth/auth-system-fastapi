from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.router_dependencies import (
    current_user_is_higher_than_target,
    get_current_user_dependency,
    get_user_repository,
    require_min_permission_level,
    superuser_only,
)
from app.core.constants import LEAD_MODERATOR
from app.models.user import UserModel
from app.schemas import (
    ReadUserSchemaAdmin,
)
from app.schemas.role_schemas import UpdateRoleSchema
from app.use_cases import (
    add_role_to_user,
    remove_role_from_user,
)
from app.use_cases.update_role_use_case import update_role_permission_level_use_case
from auth.ports.user_repository import UserRepositoryProtocol
from app.db.dependencies import get_async_session
from app.models.role import RoleModel
from app.core.constants import ROLE_NOT_FOUND


router = APIRouter(
    prefix='/admins',
    tags=['admin'],
)

@router.patch(
    '/users/{user_id}/roles/{role_id}',
    response_model=ReadUserSchemaAdmin
)
async def add_user_role_by_admin(
    role_id: int,
    _: None = Depends(
        require_min_permission_level(min_level=LEAD_MODERATOR)
    ),
    current_user: UserModel = Depends(get_current_user_dependency),
    user_repository: UserRepositoryProtocol = Depends(get_user_repository),
    target_user: UserModel = Depends(current_user_is_higher_than_target),
):
    """
    Эндпоинт для добавления роли пользователю.

    Параметры:
      - role_id: id роли, которая будет добавлена пользователю.
      - current_user: текущий пользователь, отправитель запроса. Нужен для
        передачи в use case. Fastapi хэширует результаты зависимостей.
      - user_repository: репозиторий пользователей, передается в use case.
      - target_user: пользователь, которому будет добавлена роль. передается в
        use case.
    """
    updated_user = await add_role_to_user(
        current_user=current_user,
        orm_user_obj=target_user,
        role_id=role_id,
        user_repository=user_repository,
    )
    return updated_user


@router.delete(
    '/users/{user_id}/roles/{role_id}',
    response_model=ReadUserSchemaAdmin
)
async def delete_role_from_user(
    role_id: int,
    _: None = Depends(
        require_min_permission_level(min_level=LEAD_MODERATOR)
    ),
    current_user: UserModel = Depends(get_current_user_dependency),
    user_repository: UserRepositoryProtocol = Depends(get_user_repository),
    target_user: UserModel = Depends(current_user_is_higher_than_target),
):
    """
    Эндпоинт для удаления роли у пользователя.

    Параметры:
      - role_id: id роли, которая будет добавлена пользователю.
      - current_user: текущий пользователь, отправитель запроса. Нужен для
        передачи в use case. Fastapi хэширует результаты зависимостей.
      - user_repository: репозиторий пользователей, передается в use case.
      - target_user: пользователь, которому будет добавлена роль. передается в
        use case.
    """
    updated_user = await remove_role_from_user(
        current_user=current_user,
        orm_user_obj=target_user,
        role_id=role_id,
        user_repository=user_repository,
    )
    return updated_user


@router.patch(
    '/roles/{role_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def change_role_permission_level(
    role_id: int,
    role_schema: UpdateRoleSchema,
    user_repository: UserRepositoryProtocol = Depends(get_user_repository),
    _: None = Depends(superuser_only),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Изменяет уровень доступа(permission_level) у роли.

    Доступ только для суперпользователя.
    """
    session = user_repository.get_session()
    await update_role_permission_level_use_case(
        role_id=role_id,
        role_new_permission_level=role_schema.permission_level,
        session=session,
    )
    return None
