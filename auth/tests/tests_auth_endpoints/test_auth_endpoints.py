import pytest

from fastapi import status

from auth.tests.constants import (
    TEST_VALID_TOKEN
)


@pytest.mark.asyncio
async def test_logout_success(
    async_client,
    orm_user_obj,
) -> None:
    headers = {
        'Authorization': f'Bearer {TEST_VALID_TOKEN}'
    }
    response = await async_client.post(
        '/test_auth/logout',
        headers=headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b''
