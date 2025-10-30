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

from fastapi import APIRouter, Depends, HTTPException, Header, status, Response
from jose import JWTError

from auth.abstractions import AbstractUserModel
from auth.ports.user_repository import UserRepositoryProtocol
from auth.security import (
    DEFAULT_HASHER,
    PasswordHasher,
    TokenService,
)
from auth.schemas.auth import (
    CreateUserSchemaT,
    LoginRequestSchemaT,
    LoginResponseSchemaT,
    ReadUserSchemaT,
    UpdateUserSchemaT,
)
from auth.schemas.auth_schemas import AuthSchemas
from auth.usecases import (
    register_user,
    update_user_profile,
    authenticate_user,
)


def create_auth_router(
    user_repository_dependency: Callable[..., UserRepositoryProtocol],
    *,
    token_service: TokenService,
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

    token_service_dependency = provide_token_service(token_service)

    async def require_owner(
        authorization: str = Header(...),
        token_service: TokenService = Depends(
            token_service_dependency
        ),
        user_repository: UserRepositoryProtocol = Depends(
            user_repository_dependency
        ),
    ):
        """
        Зависимость, проверяющая токен на валидность
        и возвращающая пользователя.
        """
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


    @router.patch(
        '/users/me/',
        response_model=schemas.read,
        status_code=status.HTTP_200_OK,
    )
    async def update_me(
        user_schema: schemas.update,  # type: ignore[valid-type]
        current_user: AbstractUserModel = Depends(require_owner),
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

    return router
