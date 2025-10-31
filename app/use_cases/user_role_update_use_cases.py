from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.core.constants import (
     APPLY_ROLE_TO_USER_ERROR,
     ROLE_NOT_FOUND,
     USER_NOT_FOUND
)
from app.models.user import UserModel
from auth.ports.user_repository import UserRepositoryProtocol

from app.crud import (
    role_crud,
    admin_manager_crud,
)


async def add_role_to_user(
        user_id: int,
        role_id: int,
        user_repository: UserRepositoryProtocol,
    ) -> UserModel:
        """
        Добавляет связь между пользователем и ролью.
        """
        session = user_repository._session

        orm_user_obj = await user_repository.get_user_by_id(user_id)
        if orm_user_obj is None:
            raise HTTPException(
                detail=USER_NOT_FOUND.format(user_id=user_id),
                status_code=status.HTTP_404_NOT_FOUND,
            )
        orm_role_obj = await role_crud.get_role(
            role_id=role_id,
            session=session,
        )
        if orm_role_obj is None:
            raise HTTPException(
                detail=ROLE_NOT_FOUND.format(role_id=role_id),
                status_code=status.HTTP_404_NOT_FOUND,
            )
        try:
            await admin_manager_crud.add_role(
                user=orm_user_obj,
                role=orm_role_obj,
                session=session,
            )
            await user_repository.commit()
        except SQLAlchemyError as e:
            await user_repository.rollback()
            raise HTTPException(
                detail=APPLY_ROLE_TO_USER_ERROR.format(
                     role_id=role_id, user_id=user_id
                ),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ) from e
        return orm_user_obj


async def remove_role_from_user(
        user_id: int,
        role_id: int,
        user_repository: UserRepositoryProtocol,
    ) -> UserModel:
        """
        Удаляет связь пользователя с ролью.
        """
        session = user_repository._session

        orm_user_obj = await user_repository.get_user_by_id(user_id)
        if orm_user_obj is None:
            raise HTTPException(
                detail=USER_NOT_FOUND.format(user_id=user_id),
                status_code=status.HTTP_404_NOT_FOUND,
            )
        orm_role_obj = await role_crud.get_role(
            role_id=role_id,
            session=session,
        )
        if orm_role_obj is None:
            raise HTTPException(
                detail=ROLE_NOT_FOUND.format(role_id=role_id),
                status_code=status.HTTP_404_NOT_FOUND,
            )
        try:
            await admin_manager_crud.remove_role_from_user(
                user=orm_user_obj,
                role=orm_role_obj,
                session=session,
            )
            await user_repository.commit()
        except SQLAlchemyError as e:
            await user_repository.rollback()
            raise HTTPException(
                detail=APPLY_ROLE_TO_USER_ERROR.format(
                    role_id=role_id, user_id=user_id
                ),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ) from e
        return orm_user_obj
