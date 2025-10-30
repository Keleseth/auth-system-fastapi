"""
Фабрики зависимостей для внедрения в роутер аутентификации и
предоставления отдельными компонентами в приложение FastAPI.
"""
from typing import Any, Callable

from fastapi import Depends, HTTPException, Header
from jose import JWTError

from auth.services.security.token_service import TokenServiceProtocol


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
    ) -> Any:
        token = authorization.removeprefix('Bearer ').strip()
        try:
            payload = token_service.decode_access(token)
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )
        try:
            user = await user_repository.get_user_by_id(payload.get('sub'))
        except Exception:
            raise HTTPException(
                status_code=401,
                detail='Пользователь не найден'
            )
        return user
    return get_current_user