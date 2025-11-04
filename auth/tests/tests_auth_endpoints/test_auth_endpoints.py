import pytest

from fastapi import status

from auth.services.constants import AUTH_PREFIX, LOGOUT_PREFIX
from auth.tests.constants import (
    TEST_INACTIVE_USER,
    TEST_INVALID_TOKEN,
    TEST_USER_EMAIL,
    TEST_USER_NOT_FOUND,
    TEST_VALID_TOKEN,
    TOKEN_TYPE,
)


@pytest.mark.parametrize(
    'request_type, expected_status',
    [
        (TEST_VALID_TOKEN, status.HTTP_204_NO_CONTENT),
        (TEST_INVALID_TOKEN, status.HTTP_401_UNAUTHORIZED),
        (TEST_INACTIVE_USER, status.HTTP_403_FORBIDDEN),
        (TEST_USER_NOT_FOUND, status.HTTP_401_UNAUTHORIZED),
    ]
)
@pytest.mark.asyncio
async def test_endpoint_logout_success_(
    async_client,
    request_type,
    expected_status,
) -> None:
    headers = {
        'Authorization': f'{TOKEN_TYPE} {request_type}'
    }
    response = await async_client.post(
        f'{AUTH_PREFIX}{LOGOUT_PREFIX}',
        headers=headers
    )
    assert response.status_code == expected_status
    if response.status_code == status.HTTP_204_NO_CONTENT:
        assert response.content == b''
    else:
        assert 'detail' in response.json()


@pytest.mark.parametrize(
    'user_data, expected_status',
    [
        (
            {
                'email': TEST_USER_EMAIL,
                'password': 'some_password',
                'first_name': 'Василий',
                'patronymic': 'Алибабаевич',
            },
            status.HTTP_201_CREATED
        ),
        (
            {
                'email': TEST_USER_EMAIL,
                'password': 'some_password',
                'first_name': 'Федя',
                'last_name': 'Ермаков',
                'patronymic': 'Косой',
            },
            status.HTTP_400_BAD_REQUEST
        ),
        (
            {
                'email': TEST_USER_EMAIL,
                'first_name': 'Доцент',
                'last_name': '',
            },
            status.HTTP_400_BAD_REQUEST
        ),

    ]
)
@pytest.mark.asyncio
async def test_endpoint_register_new_user(
    async_client,
) -> None:
    pass
