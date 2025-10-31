from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.base import ModelType
from app.models.role import RoleModel


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


role_crud = RoleCRUD(RoleModel)
