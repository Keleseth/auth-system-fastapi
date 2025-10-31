from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserModel

if TYPE_CHECKING:
    from app.models.role import RoleModel


class AdminManagerCRUD:
    """
    Репозиторий для управления пользователями администратором.
    """

    def __init__(
        self,
        model
    ):
        self.model = model

    async def add_role(
        self,
        user: UserModel,
        role: 'RoleModel',
        session: AsyncSession
    ) -> None:
        """
        Добавляет связь между пользователем и ролью.
        """
        if role not in user.roles:
            user.roles.append(role)
            await session.flush() 

    async def remove_role_from_user(
            self,
            user: UserModel,
            role: 'RoleModel',
            session: AsyncSession
    ):
        """
        Удаляет связь пользователя с ролью.
        """
        if role in user.roles:
            user.roles.remove(role)
            await session.flush()


admin_manager_crud = AdminManagerCRUD(UserModel)
