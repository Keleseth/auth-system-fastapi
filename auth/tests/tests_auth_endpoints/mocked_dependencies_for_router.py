from dataclasses import dataclass
from uuid import UUID

from fastapi import HTTPException, Header, status

from auth.services.constants import (
    INACTIVE_USER,
    INVALID_ACCESS_TOKEN_ERROR,
    USER_NOT_FOUND_ERROR
)
from auth.tests.constants import (
    MOCKED_TOKEN,
    TEST_INACTIVE_USER,
    TEST_INVALID_TOKEN,
    TEST_VALID_TOKEN
)


@dataclass
class MockedUserModel:
    id: UUID = 'c50eb804-131d-4cde-a504-cea137c00dc6'
    email: str = 'active@yandex.ru'
    hashed_password: str = 'some_hashed_password'
    is_active: bool = True
    token_version: int = 0
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None


@dataclass(slots=True, frozen=True)
class MockedTokenService:

    def provide_access_token(
    ) -> str:
        return MOCKED_TOKEN

    def decode_access(self, token: str) -> dict[str, dict]:
        return {
            'sub': 'c50eb804-131d-4cde-a504-cea137c00dc6',
            'token_version': 1
        }


token_service = MockedTokenService()


class MockedUserRepository:
    async def get_user_by_id(
            self,
            id=UUID('c50eb804-131d-4cde-a504-cea137c00dc6')
    ):
        return MockedUserModel(
            id=id,
            email='test@yandex.ru',
            hashed_password='some_hashed_password',
            is_active=True,
            token_version=1
        )

    async def get_by_email(self, email='test@yandex.ru'):
        return MockedUserModel(
            id=UUID('c50eb804-131d-4cde-a504-cea137c00dc6'),
            email=email,
            hashed_password='some_hashed_password',
            is_active=True,
            token_version=1
        )


def get_user_repository() -> MockedUserRepository:
    return MockedUserRepository()

def mock_get_current_user(
    authorization: str = Header(),
) -> MockedUserModel:
    authorization = authorization.removeprefix('Bearer').strip()
    if authorization == TEST_INVALID_TOKEN:
        raise HTTPException(
            detail=INVALID_ACCESS_TOKEN_ERROR,
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    elif authorization == TEST_INACTIVE_USER:
        raise HTTPException(
            detail=INACTIVE_USER,
            status_code=status.HTTP_403_FORBIDDEN
        )
    elif authorization == TEST_VALID_TOKEN:
        return MockedUserModel(
            id=UUID('c50eb804-131d-4cde-a504-cea137c00dc6'),
            email='test@yandex.ru',
            hashed_password='some_hashed_password',
            is_active=True,
            token_version=1
        )
    else:
        raise HTTPException(
            detail=USER_NOT_FOUND_ERROR,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


