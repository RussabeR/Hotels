from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.schemas.hotels_schema import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel
