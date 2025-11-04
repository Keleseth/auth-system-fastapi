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
from auth.services.constants import (
    AUTH_PREFIX,
    LOGIN_PREFIX,
    LOGOUT_PREFIX,
    REGISTER_PREFIX,
    SOFT_DELETE_USER_PREFIX,
    UPDATE_PROFILE_PREFIX,
)
from auth.services.security import (
    DEFAULT_HASHER,
    PasswordHasher,
    TokenService,
    TokenServiceProtocol,
)
from auth.schemas.user_auth_schemas import (
    CreateUserSchemaT,
    LoginRequestSchemaT,
    LoginResponseSchemaT,
    ReadUserSchemaT,
    UpdateUserSchemaT,
)
from auth.schemas.schemas_container import AuthSchemas
from auth.usecases import (
    authenticate_use_case_dependency,
    logout_use_case_dependency,
    register_use_case_dependency,
    soft_delete_use_case_dependency,
    update_profile_use_case_dependency,
)
from auth.api.v1.dependencies import (
    build_get_current_user_dependency
)


def create_auth_router(
    *,
    user_repository_dependency: Callable[..., UserRepositoryProtocol],
    token_service: TokenServiceProtocol,
    schemas: AuthSchemas[
        CreateUserSchemaT,
        LoginRequestSchemaT,
        LoginResponseSchemaT,
        ReadUserSchemaT,
        UpdateUserSchemaT,
    ] = AuthSchemas(),
    password_hasher: PasswordHasher = DEFAULT_HASHER,
    prefix: str = AUTH_PREFIX,
    tags: list[str] | None = None,
    test_mode: bool = False,
    _mock_get_current_user: Callable[..., UserModelTypeHint] | None = None,

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
    - test_mode - флаг для отладки и подмены внутрефабричных
    зависимостей моками.
    - _mock_get_current_user - мок зависимость получения текущего пользователя
    P.S. _mock_get_current_user нужен только для тестов внутри библиотеки,
    и будет заменен в обновлениях на внедрение глобальной зависимости.
    """

    router = APIRouter(prefix=prefix, tags=tags)

    def provide_token_service(token_service: TokenServiceProtocol):
        def _dependency() -> TokenServiceProtocol:
            return token_service
        return _dependency

    # Зависимость для внедрения сервиса работы с токенами
    token_service_dependency = provide_token_service(token_service)

    # Mock зависимость получения текущего пользователя для тестов
    if test_mode and _mock_get_current_user is not None:
        get_current_user = _mock_get_current_user
    else:
        # Зависимость получения текущего аутентифицированного пользователя
        get_current_user = build_get_current_user_dependency(
            token_service_dependency=token_service_dependency,
            user_repository_dependency=user_repository_dependency,
        )

    @router.post(
        REGISTER_PREFIX,
        response_model=schemas.read,
        status_code=status.HTTP_201_CREATED,
    )
    async def register(
        user_schema: schemas.create,  # type: ignore[valid-type]
        user_repository: UserRepositoryProtocol = Depends(
            user_repository_dependency
        ),
        register_user: Callable = Depends(
            register_use_case_dependency
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
        LOGIN_PREFIX,
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
        authenticate_user: Callable = Depends(
            authenticate_use_case_dependency
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
        LOGOUT_PREFIX,
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def logout(
        current_user: UserModelTypeHint = Depends(get_current_user),
        user_repository: UserRepositoryProtocol = Depends(
            user_repository_dependency
        ),
        logout_user: Callable = Depends(
            logout_use_case_dependency
        ),
    ):
        await logout_user(
            orm_user_obj=current_user,
            user_repository=user_repository,
        )


    @router.patch(
        UPDATE_PROFILE_PREFIX,
        response_model=schemas.read,
        status_code=status.HTTP_200_OK,
    )
    async def update_me(
        user_schema: schemas.update,  # type: ignore[valid-type]
        current_user: UserModelTypeHint = Depends(get_current_user),
        user_repository: UserRepositoryProtocol = Depends(
            user_repository_dependency
        ),
        update_user_profile: Callable = Depends(
            update_profile_use_case_dependency
        ),
    ):
        user = await update_user_profile(
            user_repository=user_repository,
            orm_user_obj=current_user,
            **user_schema.model_dump(exclude_none=True),
        )
        return user


    @router.delete(
        SOFT_DELETE_USER_PREFIX,
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def soft_delete_me(
        current_user: UserModelTypeHint = Depends(get_current_user),
        user_repository: UserRepositoryProtocol = Depends(
            user_repository_dependency
        ),
        soft_delete: Callable = Depends(
            soft_delete_use_case_dependency
        ),
    ):
        await soft_delete(
            orm_user_obj=current_user,
            user_repository=user_repository,
        )

    return router
