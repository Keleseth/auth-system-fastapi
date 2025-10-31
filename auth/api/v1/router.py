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
        user_model: Any = UserModel,
        session: AsyncSession = Depends(get_async_session),
    ) -> UserRepositoryProtocol:
        return SQLAlchemyUserRepository(
            session=session,
            user_model=user_model
        )
"""
from typing import Callable

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from auth.abstractions import UserModelTypeHint
from auth.ports.user_repository import UserRepositoryProtocol
from auth.services.security import (
    DEFAULT_HASHER,
    PasswordHasher,
    TokenService,
)
from auth.schemas.user_auth_schemas import (
    CreateUserSchemaT,
    LoginRequestSchemaT,
    LoginResponseSchemaT,
    ReadUserSchemaT,
    UpdateUserSchemaT,
)
from auth.schemas.schemas_container import AuthSchemas
from auth.services.security.token_service import (
    TokenService,
    TokenServiceProtocol,
)
from auth.usecases import (
    register_user,
    update_user_profile,
    authenticate_user,
)
from auth.api.v1.dependencies import (
    build_get_current_user_dependency
)
from auth.usecases.admin_update_user_use_case import update_user_role
from auth.usecases.logout_user_use_case import logout_user
from auth.usecases.soft_delete_use_case import soft_delete_usecase


def create_auth_router(
    user_repository_dependency: Callable[..., UserRepositoryProtocol],
    *,
    token_service: TokenServiceProtocol,
    schemas: AuthSchemas[
        CreateUserSchemaT,
        LoginRequestSchemaT,
        LoginResponseSchemaT,
        ReadUserSchemaT,
        UpdateUserSchemaT,
    ] = AuthSchemas(),
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
    - token_service: Класс для работы с JWT-токенами с настраиваемыми
    (обязательными) параметрами.
    - schemas: контейнер с классами схем (create/read),
    допускаются наследники дефолтных схем.
    - password_hasher: реализация интерфейса PasswordHasher. 
    DEFAULT_HASHER - дефолтная реализация PasswordHasher.
    - prefix/tags: стандартные параметры APIRouter.
    """

    router = APIRouter(prefix=prefix, tags=tags)

    def provide_token_service(token_service: TokenService):
        def _dependency() -> TokenService:
            return token_service
        return _dependency

    # Зависимость для внедрения сервиса работы с токенами
    token_service_dependency = provide_token_service(token_service)

    # TODO протокольную аннотацию Depends не пропускает. Обойти
    get_current_user = build_get_current_user_dependency(
        token_service_dependency=token_service_dependency,
        user_repository_dependency=user_repository_dependency,
    )

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
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Регистрация не удалась.'
            )

        return user

    @router.post(
        '/login',
        response_model=schemas.login_response,
        status_code=status.HTTP_200_OK,
    )
    async def login(
        user_schema: schemas.login_request,  # type: ignore[valid-type]
        user_repository: UserRepositoryProtocol = Depends(
            user_repository_dependency
        ),
        token_service: TokenService = Depends(
            token_service_dependency
        ),
    ):
        data = user_schema.model_dump()
        token = await authenticate_user(
            user_repository=user_repository,
            hasher=password_hasher,
            token_service=token_service,
            email=data.get('email'),
            password=data.get('password'),
        )
        return {'access_token': token, 'token_type': 'bearer'}


    @router.post(
        '/logout',
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def logout(
        current_user: UserModelTypeHint = Depends(get_current_user),
        user_repository: UserRepositoryProtocol = Depends(
            user_repository_dependency
        ),
    ):
        await logout_user(
            current_user=current_user,
            user_repository=user_repository,
        )


    @router.patch(
        '/users/me/',
        response_model=schemas.read,
        status_code=status.HTTP_200_OK,
    )
    async def update_me(
        user_schema: schemas.update,  # type: ignore[valid-type]
        current_user: UserModelTypeHint = Depends(get_current_user),
        user_repository: UserRepositoryProtocol = Depends(
            user_repository_dependency
        ),
    ):
        user = await update_user_profile(
            user_repository=user_repository,
            orm_user_obj=current_user,
            **user_schema.model_dump(exclude_none=True),
        )
        return user


    @router.post(
        '/users/me/delete',
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def soft_delete_me(
        current_user: UserModelTypeHint = Depends(get_current_user),
        user_repository: UserRepositoryProtocol = Depends(
            user_repository_dependency
        ),
    ):
        await soft_delete_usecase(
            user=current_user,
            user_repository=user_repository,
        )

    return router
