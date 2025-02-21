from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORrm


class RoomsRepository(BaseRepository):
    model = RoomsORrm
