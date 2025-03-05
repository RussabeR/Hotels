from pydantic import BaseModel, ConfigDict


class RoomAddRequest(BaseModel):
    title: str
    price: int
    quantity: int
    description: str | None = None
    facilities_ids: list[int] | None = None


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    price: int
    quantity: int
    description: str | None = None


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPatchRequest(BaseModel):
    title: str | None = None
    price: int | None = None
    quantity: int | None = None
    description: str | None = None
    facilities_ids: list[int] | None = None


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    price: int | None = None
    quantity: int | None = None
    description: str | None = None
    facilities_ids: list[int] | None = None
