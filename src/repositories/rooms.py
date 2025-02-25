from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORrm
from src.schemas.rooms_schema import Room


class RoomsRepository(BaseRepository):
    model = RoomsORrm
    schema = Room
