import pytest

from auth.domain.constants import (
    FIRST_NAME_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH,
    PATRONYMIC_MAX_LENGTH
)
from auth.domain.entities.user import User
from auth.domain.exceptions import (
    InvalidUserDataError,
    UserInactiveError
)


@pytest.mark.parametrize(
    'first_name, last_name, patronymic, raise_exception',
    [
        ('Newname', 'Newlastname', 'Newpatronymic', False),
        ('', 'Newlastname', 'Newpatronymic', True),
        (
            'a' * (FIRST_NAME_MAX_LENGTH + 1),
            'Newlastname', 'Newpatronymic',
            True
        ),
        ('Newname', '', 'Newpatronymic', True),
        (
            'Newname',
            'a' * (LAST_NAME_MAX_LENGTH + 1),
            'Newpatronymic',
            True
        ),
        ('Newname', 'Newlastname', '', True),
        (
            'Newname',
            'Newlastname',
            'a' * (PATRONYMIC_MAX_LENGTH + 1),
            True
        ),
    ]
)
def test_active_user_can_update_profile(
    active_user_with_fio,
    first_name,
    last_name,
    patronymic,
    raise_exception
) -> None:
    if raise_exception:
        with pytest.raises(InvalidUserDataError):
            active_user_with_fio.update_profile(
                first_name=first_name,
                last_name=last_name,
                patronymic=patronymic
            )
    else:
        active_user_with_fio.update_profile(
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic
        )
        assert active_user_with_fio.first_name == first_name
        assert active_user_with_fio.last_name == last_name
        assert active_user_with_fio.patronymic == patronymic


def test_invalid_email_format(
    domain_user_class: type[User],
) -> None:
    with pytest.raises(InvalidUserDataError):
        domain_user_class(
        email=' EXPECTO_PATRONUM ',
        hashed_password='some_hashed_password',
    )


def test_active_user_can_authenticate(
    active_user_with_fio,
) -> None:
    active_user_with_fio.verify_user_can_authenticate()


def test_active_user_can_soft_delete(
    active_user_with_fio,
) -> None:
    active_user_with_fio.soft_delete()
    assert not active_user_with_fio.is_active
    assert active_user_with_fio.deleted_at is not None


def test_inactive_user_cannot_authenticate(
    inactive_user,
) -> None:
    with pytest.raises(UserInactiveError):
        inactive_user.verify_user_can_authenticate()


def test_inactive_user_cannot_update_profile(
    inactive_user
) -> None:
    with pytest.raises(UserInactiveError):
        inactive_user.update_profile(
            first_name='Newname',
            last_name='Newlastname',
            patronymic='Newpatronymic'
        )


def test_inactive_user_cannot_soft_delete(
    inactive_user
) -> None:
    with pytest.raises(UserInactiveError):
        inactive_user.soft_delete()
