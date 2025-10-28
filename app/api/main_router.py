from fastapi import APIRouter

from auth.api.router import create_auth_router
from app.db.dependencies import get_user_repository

router = APIRouter(
    prefix='/v1',
)

auth_router = create_auth_router(
    user_repository_dependency=get_user_repository,
    prefix='/testing_auth',
    tags=['test1']
)

router.include_router(auth_router)
