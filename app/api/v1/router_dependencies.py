"""
Продублированы зависимости.
TODO в библиотеке дать возможность передавать в фабрику роутера
как объекты для зависимостей, так и фабрики зависимостей.
"""
from datetime import timedelta
from typing import Any, Callable
from fastapi import Depends, HTTPException, Header, status
from jose import JWTError

from app.core.config import settings
from app.db.dependencies import get_user_repository
from app.models.mock_data import mock_objects, MockData
from auth.api.v1.dependencies import build_get_current_user_dependency
from auth.services.constants import INVALID_ACCESS_TOKEN_ERROR, USER_NOT_FOUND_ERROR
from auth.services.security.token_service import TokenService, TokenServiceProtocol


def provide_from_instance(obj):
    def _dep():
        return obj
    return _dep


token_service = TokenService(
    secret=settings.JWT_SECRET_KEY,
    algorithm=settings.JWT_ALGORITHM,    
    access_ttl=timedelta(minutes=settings.JWT_ACCESS_TOKEN_LIFESPAN),
)
token_service_dependency = provide_from_instance(token_service)


def get_mock_data():
    return mock_objects


def build_get_current_user_dependency(
    *,
    token_service_dependency: Callable[..., TokenServiceProtocol],
    user_repository_dependency: Callable[..., Any],
):
    async def get_current_user(
        authorization: str = Header(),
        token_service: TokenServiceProtocol = Depends(
            token_service_dependency
        ),
        user_repository: Any = Depends(
            user_repository_dependency
        ),
    ) -> Callable[[], Any]:
        token = authorization.removeprefix('Bearer ').strip()
        try:
            payload = token_service.decode_access(token)
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail=INVALID_ACCESS_TOKEN_ERROR
            )
        try:
            user = await user_repository.get_user_by_id(payload.get('sub'))
        except Exception:
            raise HTTPException(
                status_code=401,
                detail=USER_NOT_FOUND_ERROR
            )
        return user
    return get_current_user

get_current_user_dependency = build_get_current_user_dependency(
    token_service_dependency=token_service_dependency,
    user_repository_dependency=get_user_repository
)


async def author_or_admin_only(
    id,
    current_user = Depends(get_current_user_dependency),
    mock_objects: dict[str, MockData] = Depends(get_mock_data)
):
    current_user_id = str(current_user.id)
    chocolate = mock_objects.get(id)
    if chocolate is None:
        raise HTTPException(
            detail='Искомый объект отсутствует',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    is_admin = any(role.name == 'admin' for role in current_user.roles)
    if current_user_id != chocolate.user_id and not is_admin:
        raise HTTPException(
            detail='Недостаточно прав',
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return chocolate
