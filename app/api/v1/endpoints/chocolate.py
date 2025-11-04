from fastapi import APIRouter, Depends

from app.api.v1.router_dependencies import (
    author_or_min_permission_level,
    get_chocolate_dependency,
)
from app.core.constants import LEAD_MODERATOR
from app.models.mock_data import MockData
from app.schemas.mock_schemas import ReadMockDataChocolate


router = APIRouter(
    prefix='/chocolates',
    tags=['chocolates']
)

@router.get(
    '/{chocolate_id}',
    response_model=ReadMockDataChocolate
)
async def get_chocolate(
    chocolate_id: int,
    object: MockData = Depends(
        author_or_min_permission_level(
            resource_dependency=get_chocolate_dependency,
            min_level=LEAD_MODERATOR,
            author_attr='user_id',
        )
    )
):
    """
    Эндпоинт для получения шоколадки!

    Доступ для автора или пользователей с уровнем прав не ниже LEAD_MODERATOR.
    """
    return ReadMockDataChocolate(chocolate=object.chocolate)
