

from uuid import UUID
from fastapi import APIRouter, Depends


from app.api.v1.router_dependencies import (
    admin_only,
    get_user_repository
)
from app.schemas import (
    ReadUserSchemaAdmin,
)
from app.use_cases import (
    add_role_to_user,
    remove_role_from_user,
)


router = APIRouter(
    prefix='/admins',
    tags=['admin'],
)

@router.patch(
    '/users/{user_id}/roles/{role_id}',
    response_model=ReadUserSchemaAdmin
)
async def add_user_role_by_admin(
    user_id: UUID,
    role_id: int,
    _: None = Depends(admin_only),
    user_repository=Depends(get_user_repository),
):
    updated_user = await add_role_to_user(
        user_id=user_id,
        role_id=role_id,
        user_repository=user_repository,
    )
    return updated_user


@router.delete(
    '/users/{user_id}/roles/{role_id}',
    response_model=ReadUserSchemaAdmin
)
async def delete_role_from_user(
    user_id: UUID,
    role_id: int,
    _: None = Depends(admin_only),
    user_repository=Depends(get_user_repository),
):
    updated_user = await remove_role_from_user(
        user_id=user_id,
        role_id=role_id,
        user_repository=user_repository,
    )
    return updated_user
