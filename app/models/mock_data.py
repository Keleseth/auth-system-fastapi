from dataclasses import dataclass
from uuid import UUID

from app.core.config import settings

@dataclass(slots=True, frozen=True)
class MockData:
    """
    Класс для хранения и предоставления моковых данных
    для тестирования и разработки.
    """

    chocolate_id: int
    user_id: UUID
    chocolate: str


mock_objects: dict[str, MockData] = {str(i):
    MockData(
        chocolate_id=i,
        user_id=settings.AUTHOR_USER_UUID,
        chocolate='марс' if i==1 else ('сникерс' if i==2 else 'твикс')
    ) for i in range(1, 4)
}
