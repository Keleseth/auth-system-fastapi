from fastapi import APIRouter, Depends

from app.api.v1.router_dependencies import (
    token_service,
    author_or_admin_only
)

from app.db.dependencies import get_user_repository
from app.models.mock_data import MockData
from app.schemas.mock_schemas import ReadMockDataChocolate
from auth.api.v1.router import create_auth_router

router = APIRouter(
    prefix='/v1',
)

auth_router = create_auth_router(
    user_repository_dependency=get_user_repository,
    token_service=token_service,
    prefix='/testing_auth',
    tags=['test1']
)

router.include_router(auth_router)

@router.get(
    '/chocolates/{id}',
    response_model=ReadMockDataChocolate
)
async def get_chocolate(
    id: str,
    object: MockData = Depends(author_or_admin_only)
):
    return ReadMockDataChocolate(chocolate=object.chocolate)
