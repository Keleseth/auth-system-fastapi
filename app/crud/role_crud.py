from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.base import ModelType
from app.models.role import RoleModel
from auth.exceptions.custom_exceptions import RepositoryError


class RoleCRUD:

    def __init__(self, model: Type[ModelType]):
        self.model = model


    async def get_role(
        self,
        role_id: int,
        session: AsyncSession,
    ) -> RoleModel | None:
        """
        Получает роль по id.
        """
        query = select(self.model).where(self.model.id == role_id)
        result = await session.execute(query)
        return result.scalars().first()

    async def change_role_permission_level(
        self,
        role: RoleModel,
        new_permission_level: int,
        session: AsyncSession,
    ) -> RoleModel:
        """
        Изменяет уровень доступа у роли.
        """
        role.permission_level = new_permission_level
        session.add(role)

    async def commit_changes(
        self,
        session: AsyncSession,
    ) -> None:
        """
        Фиксирует изменения в сессии.
        """
        try:
            await session.commit()
        except RepositoryError as error:
            await session.rollback()
            raise RepositoryError(
                'Ошибка завершения транзакции'
            ) from error


role_crud = RoleCRUD(RoleModel)
