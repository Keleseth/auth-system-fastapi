"""
TODO докстринг модуля.
Фабрика ожидает следующие параметр user_repository_dependency:
Depends склеивающая фабрика - возвращающая
объект типа UserRepositoryProtocol для доступа к данным пользователей.

Пример для SQLAlchemy:
    engine = create_async_engine(settings.database_url)

    AsyncSessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
        async with AsyncSessionLocal() as async_session:
            yield async_session


    def get_user_repository(
        user_model: type[UserModelProtocol] = UserModel,
        session: AsyncSession = Depends(get_async_session),
    ) -> UserRepositoryProtocol:
        return SQLAlchemyUserRepository(
            session=session,
            user_model=user_model
        )
"""
from typing import Callable

from fastapi import APIRouter, Depends, HTTPException, status

from auth.usecases import (
    register_user,
    update_user_profile,
)
from auth.ports.user_repository import UserRepositoryProtocol
from auth.schemas.auth import (
    CreateUserSchemaT,
    ReadUserSchemaT,
)
from auth.schemas.auth_schemas import AuthSchemas
from auth.security.password import DEFAULT_HASHER, PasswordHasher


def create_auth_router(
    user_repository_dependency: Callable[..., UserRepositoryProtocol],
    *,
    schemas: AuthSchemas[CreateUserSchemaT, ReadUserSchemaT] = AuthSchemas(),
    password_hasher: PasswordHasher = DEFAULT_HASHER,
    prefix: str = '/auth',
    tags: list[str] | None = None,
    ) -> APIRouter:
    """
    Фабрика роутера для системы аутентификации и авторизации.
    Возвращает роутер системы аутентификации для подключения.

    Параметры:
    - user_repository_dependency: Depends-фабрика,
    возвращающая UserRepositoryProtocol для доступа к данным пользователей.
    Сессия вшита в объект репозитория.
    - schemas: контейнер с классами схем (create/read),
    допускаются наследники дефолтных схем.
    - password_hasher: реализация интерфейса PasswordHasher. 
    DEFAULT_HASHER - дефолтная реализация PasswordHasher.
    - prefix/tags: стандартные параметры APIRouter.
    """

    router = APIRouter(prefix=prefix, tags=tags)

    @router.post(
        '/register',
        response_model=schemas.read,
        status_code=status.HTTP_201_CREATED,
    )
    async def register(
        user_schema: schemas.create,  # type: ignore[valid-type]
        user_repository: UserRepositoryProtocol = Depends(
            user_repository_dependency
        ),
    ):
        user = await register_user(
            user_repository=user_repository,
            hasher=password_hasher,
            **user_schema.model_dump(exclude_none=True),
        )

        if user is None:
            raise HTTPException(
                tatus_code=status.HTTP_400_BAD_REQUEST,
                detail='Регистрация не удалась.'
            )

        return user

    @router.patch(
        '/users/me/',
        response_model=schemas.read,
        status_code=status.HTTP_200_OK,
    )
    async def update_me(
        user_schema: schemas.create,  # type: ignore[valid-type]
        user_repository: UserRepositoryProtocol = Depends(
            user_repository_dependency
        ),
    ):
        user = await update_user_profile(
            user_repository=user_repository,
            **user_schema.model_dump(exclude_none=True),
        )

    return router
