from auth.tests.constants import MOCKED_TOKEN
from auth.tests.tests_auth_endpoints.mocked_dependencies_for_router import (
    MockedUserModel
)


def mock_authenticate_use_case():
    return MOCKED_TOKEN

def mocked_authenticate_use_case_dependency():
    return mock_authenticate_use_case

def mock_register_use_case():
    return MockedUserModel()

def mocked_register_use_case_dependency():
    return mock_register_use_case

async def mock_logout_use_case(
    *,
    orm_user_obj,
    user_repository
):
    return None

def mocked_logout_use_case_dependency():
    return mock_logout_use_case
