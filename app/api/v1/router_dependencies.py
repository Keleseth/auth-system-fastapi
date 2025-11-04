"""
Продублированы зависимости.
TODO в библиотеке дать возможность передавать в фабрику роутера
как объекты для зависимостей, так и фабрики зависимостей.
"""
from datetime import timedelta
from typing import Any, Callable
from uuid import UUID
from fastapi import Depends, HTTPException, status

from app.api.v1.utils import get_user_max_permission_level
from app.core.config import settings
from app.core.constants import LIMITED_ACCESS, OBJECT_NOT_FOUND, USER_NOT_FOUND
from app.db.dependencies import get_user_repository
from app.models import (
    mock_objects,
    MockData,
    UserModel,
)
from auth.api.v1.dependencies import (
    build_get_current_user_dependency
)
from auth.services.security.token_service import (
    TokenService,
)


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

# Фабрика build_get_current_user_dependency, но get_current_user_dependency
# вшит в роутер auth библиотеки напрямую, потому нужна своя версия в app.
get_current_user_dependency = build_get_current_user_dependency(
    token_service_dependency=token_service_dependency,
    user_repository_dependency=get_user_repository
)

def author_or_min_permission_level(
    resource_dependency: Callable[..., Any],
    min_level: int,
    author_attr: str,
) -> MockData:
    """
    Фабрика, которая создает зависимость, проверяющую право
    доступа к ресурсу, динамически передавая в нее параметры:
    - min_level: минимальный уровень прав доступа пользователя
    - author_attr: имя атрибута в модели ресурса, который хранит ссылку на
      пользователя.
    """
    async def _dependency(
        current_user: UserModel = Depends(get_current_user_dependency),
        resource: Any = Depends(resource_dependency)
    ) -> Any:
        """
        Проверяет, что текущий пользователь является автором
        запрашиваемого объекта или имеет минимальный уровень
        прав доступа. Если доступ есть, возвращает результат зависимости
        resource_dependency и передает управление дальше.

        В параметр resource ожидается зависимость, которая вернет объект
        связанный с моделью пользователя полем author_attr(user_id). Параметр
        добавлен для гибкости, чтобы работать с моделями с отличным fk на
        пользователя.
        """
        if current_user.is_superuser:
            return resource
        is_author = str(current_user.id) == str(getattr(resource, author_attr))
        if is_author or get_user_max_permission_level(current_user) >= min_level:
            return resource
        raise HTTPException(
            detail=LIMITED_ACCESS,
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return _dependency


def get_chocolate_dependency(
    chocolate_id: int,
    chocolates: dict[str, MockData] = Depends(get_mock_data),
) -> MockData:
    chocolate = chocolates.get(chocolate_id)
    if chocolate is None:
        raise HTTPException(
            detail=OBJECT_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return chocolate


async def get_target_user(
    user_id: UUID,
    user_repository = Depends(get_user_repository),
) -> UserModel:
    """
    Получает искомого пользователя по его id(UUID) переданного в
    path-параметре запроса.
    """
    target_user = await user_repository.get_user_by_id(user_id)
    if target_user is None:
        raise HTTPException(
            detail=USER_NOT_FOUND.format(user_id=user_id),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return target_user


async def current_user_is_higher_than_target(
    current_user: UserModel = Depends(get_current_user_dependency),
    target_user: UserModel = Depends(get_target_user),
) -> UserModel:
    """
    Проверяет, что отправитель запроса(current_user) имеет более высокий уровень
    доступа, чем искомый пользователь(target_user), или является суперюзером.
    """
    if (
        get_user_max_permission_level(current_user)
        <= get_user_max_permission_level(target_user)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=LIMITED_ACCESS,
        )
    return target_user


def require_min_permission_level(
    min_level: int,
) -> Callable[..., None]:
    """
    Фабрика, которая создает зависимость, проверяющую соответствует ли
    пользователь минимальному уровню прав доступа (permission_level).

    Параметры:
      - min_level: параметр фабрики, который определяет необходимый минимальный
      уровень прав для каждого отдельного эндпоинта.
    """
    async def _dependency(
        current_user: UserModel = Depends(get_current_user_dependency),
    ) -> None:
        if current_user.is_superuser or get_user_max_permission_level(current_user) >= min_level:
            return None
        raise HTTPException(
            detail=LIMITED_ACCESS,
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return _dependency


async def superuser_only(
    current_user: UserModel = Depends(get_current_user_dependency),
) -> None:
    """
    Отдельная для суперпользователя зависимость для явного ограничвения.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            detail=LIMITED_ACCESS,
            status_code=status.HTTP_403_FORBIDDEN,
        )
