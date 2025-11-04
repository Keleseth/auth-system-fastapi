from fastapi import APIRouter, Depends

from app.api.v1.router_dependencies import (
    author_or_min_level,
    get_chocolate,
)
from app.core.constants import TESTING_CHOCOLATE_PERMISSION_LEVEL
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
        author_or_min_level(
            resource_dependency=get_chocolate,
            min_level=TESTING_CHOCOLATE_PERMISSION_LEVEL,
            author_attr='user_id',
        )
    )
):
    return ReadMockDataChocolate(chocolate=object.chocolate)
