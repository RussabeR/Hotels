from pydantic import BaseModel, ConfigDict

from src.schemas.facilities_schema import Facility


class RoomAddRequest(BaseModel):
    title: str
    price: int
    quantity: int
    description: str | None = None
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    price: int
    quantity: int
    description: str | None = None


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatchRequest(BaseModel):
    title: str | None = None
    price: int | None = None
    quantity: int | None = None
    description: str | None = None
    facilities_ids: list[int] = []


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    price: int | None = None
    quantity: int | None = None
    description: str | None = None
