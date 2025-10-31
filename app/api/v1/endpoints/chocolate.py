from fastapi import APIRouter, Depends

from app.api.v1.router_dependencies import (
    author_or_admin_only
)
from app.models.mock_data import MockData
from app.schemas.mock_schemas import ReadMockDataChocolate


router = APIRouter(
    prefix='/chocolates',
    tags=['chocolates']
)

@router.get(
    '/{id}',
    response_model=ReadMockDataChocolate
)
async def get_chocolate(
    id: str,
    object: MockData = Depends(author_or_admin_only)
):
    return ReadMockDataChocolate(chocolate=object.chocolate)
