from fastapi import APIRouter

from app.api.v1.endpoints import (
    chocolate_router,
    admin_manager_router
)
from app.api.v1.router_dependencies import (
    token_service,
)

from app.db.dependencies import get_user_repository
from auth.api.v1.router import create_auth_router

router = APIRouter(
    prefix='/v1',
)

auth_router = create_auth_router(
    user_repository_dependency=get_user_repository,
    token_service=token_service,
    prefix='/testing_auth',
    tags=['test1']
)

router.include_router(auth_router)
router.include_router(chocolate_router)
router.include_router(admin_manager_router)