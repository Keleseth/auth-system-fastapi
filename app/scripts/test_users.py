from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models.user import UserModel
from app.models.role import RoleModel
from auth.services.security import DEFAULT_HASHER


async def create_admin_author_moderator(
        session: AsyncSession
) -> None:
    """
    Создает трех пользователей с данными из .env, если еще не существует.

    Дефолтные пользователи(можно переназначить через .env):
      - superuser@yandex.ru
      - admin@yandex.ru
      - author@yandex.ru
      - moderator@yandex.ru

    Берет данные из .env файла, если отсутствуют то дефолтные из settings.
    """
    roles = {
        'admin': settings.ADMIN_ROLE_NAME,
        'author': settings.AUTHOR_ROLE_NAME,
        'moderator': settings.MODERATOR_ROLE_NAME,
    }
    role_objects = {}
    for key, name in roles.items():
        result = await session.execute(
            select(RoleModel).where(RoleModel.name==name)
        )
        role = result.scalars().first()
        if not role:
            role = RoleModel(name=name)
            session.add(role)
            await session.flush()
        role_objects[key] = role

    users_data = [
        {
            'id': settings.ADMIN_USER_UUID,
            'email': settings.ADMIN_EMAIL,
            'password': settings.PASSWORD,
            'role': role_objects['admin']
        },
        {
            'id': settings.MODERATOR_USER_UUID,
            'email': settings.MODERATOR_EMAIL,
            'password': settings.PASSWORD,
            'role': role_objects['moderator']
        },
        {
            'id': settings.AUTHOR_USER_UUID,
            'email': settings.AUTHOR_EMAIL,
            'password': settings.PASSWORD,
            'role': role_objects['author']
        },
    ]
    for data in users_data:
        result = await session.execute(
            select(UserModel).where(UserModel.id == data['id'])
        )
        user = result.scalars().first()
        if not user:
            hashed_pw = DEFAULT_HASHER.hash(data['password'])
            user = UserModel(
                id=data['id'],
                email=data['email'],
                hashed_password=hashed_pw,
                is_active=True,
            )
            user.roles.append(data['role'])
            session.add(user)

    await ensure_superuser(session)
    await session.commit()


async def ensure_superuser(
        session: AsyncSession
) -> None:
    """
    Создает суперпользователя с данными из settings, если в базе еще нет
    ни одного суперпользователя.
    """
    result = await session.execute(
        select(UserModel).where(UserModel.is_superuser == True)
    )
    existing = result.scalars().first()
    if existing:
        return

    hashed_pw = DEFAULT_HASHER.hash(settings.PASSWORD)
    super_user = UserModel(
        id=settings.SUPER_USER_UUID,
        email=settings.SUPER_USER_EMAIL,
        hashed_password=hashed_pw,
        is_active=True,
        is_superuser=True,
    )
    session.add(super_user)
