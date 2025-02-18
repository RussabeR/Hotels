from repositories.base import BaseRepository
from src.models.hotels import HotelsORrm


class HotelsRepository(BaseRepository):
    model = HotelsORrm
