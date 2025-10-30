from datetime import timedelta

from fastapi import APIRouter

from app.db.dependencies import get_user_repository
from app.core.config import settings
from auth.api.router import create_auth_router
from auth.services.security.token_service import TokenService

router = APIRouter(
    prefix='/v1',
)

token_service = TokenService(
    secret=settings.JWT_SECRET_KEY,
    algorithm=settings.JWT_ALGORITHM,    
    access_ttl=timedelta(minutes=settings.JWT_ACCESS_TOKEN_LIFESPAN),
)

auth_router = create_auth_router(
    user_repository_dependency=get_user_repository,
    token_service=token_service,
    prefix='/testing_auth',
    tags=['test1']
)

router.include_router(auth_router)
