import pytest

from auth.domain.entities.user import User


@pytest.fixture
def domain_user_class() -> type[User]:
    return User


@pytest.fixture
def active_user_with_fio() -> User:
    return User(
        email='active@yandex.ru',
        hashed_password='some_hashed_password',
        is_active=True,
        first_name='Active',
        last_name='User',
        patronymic='Fixturovich'
    )


@pytest.fixture
def inactive_user() -> User:
    return User(
        email='inactive@yandex.ru',
        hashed_password='some_hashed_password',
        is_active=False,
        first_name='Inactive',
        last_name='User',
        patronymic='Fixturovich'
    )
