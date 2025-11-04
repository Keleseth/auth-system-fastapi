"""
Фабрики зависимостей для внедрения в роутер аутентификации и
предоставления отдельными компонентами в приложение FastAPI.
"""
from typing import Any, Callable

from fastapi import (
    Depends,
    HTTPException,
    Header,
    status
)
from jose import JWTError

from auth.services.constants import (
    INACTIVE_USER,
    INVALID_ACCESS_TOKEN_ERROR,
    TOKEN_TYPE,
    USER_NOT_FOUND_ERROR
)
from auth.services.security.token_service import TokenServiceProtocol


def build_get_current_user_dependency(
    *,
    token_service_dependency: Callable[..., TokenServiceProtocol],
    user_repository_dependency: Callable[..., Any],
) -> Callable[[], Any]:
    """
    Фабрика зависимости 'get_current_user' получения аутентифицированного
    пользователя после проверки токена на валидность.
    """
    async def get_current_user(
        authorization: str = Header(),
        token_service: TokenServiceProtocol = Depends(
            token_service_dependency
        ),
        user_repository: Any = Depends(
            user_repository_dependency
        ),
    ):
        token = authorization.removeprefix(TOKEN_TYPE).strip()
        try:
            payload = token_service.decode_access(token)
        except Exception:
            raise HTTPException(
                detail=INVALID_ACCESS_TOKEN_ERROR,
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        try:
            user = await user_repository.get_user_by_id(payload.get('sub'))
        except Exception:
            raise HTTPException(
                detail=USER_NOT_FOUND_ERROR,
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        if not user.is_active:
            raise HTTPException(
                detail=INACTIVE_USER,
                status_code=status.HTTP_403_FORBIDDEN
            )
        if user.token_version != payload.get('token_version'):
            raise HTTPException(
                detail=INVALID_ACCESS_TOKEN_ERROR,
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        return user
    return get_current_user
