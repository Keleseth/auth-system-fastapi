from pytest import fixture
from httpx import ASGITransport, AsyncClient

from auth.tests.tests_auth_endpoints.fastapi_app import app
from auth.tests.tests_auth_endpoints.mocked_dependencies_for_router import (
    MockedUserModel,
)


@fixture
async def async_client():
    """
    Асинхронный клиент для тестирования эндпоинтов.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url='http://test'
    ) as client:
        yield client


@fixture
def orm_user_obj():
    """
    Мок объекта пользователя по MockedUserModel.
    """
    return MockedUserModel()
