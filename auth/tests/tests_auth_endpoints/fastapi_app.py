from fastapi import FastAPI

from auth.api.v1.router import create_auth_router
from auth.services.constants import AUTH_PREFIX
from auth.tests.tests_auth_endpoints.mocked_dependencies_for_router import (
    token_service,
    mock_get_current_user,
    get_user_repository
)
from auth.tests.tests_auth_endpoints.mocked_use_cases import (
    mocked_logout_use_case_dependency,
)
from auth.usecases import (
    logout_use_case_dependency,
)



app = FastAPI(
    title='Юнит-тесты эндпоинтов',
    description='Юнит-тесты для эндпоинтов аутентификации',
)

test_auth_router = create_auth_router(
    user_repository_dependency=get_user_repository,
    token_service=token_service,
    test_mode=True,
    _mock_get_current_user=mock_get_current_user,
    prefix=AUTH_PREFIX,
)
app.include_router(test_auth_router)

app.dependency_overrides[
    logout_use_case_dependency
] = mocked_logout_use_case_dependency
 