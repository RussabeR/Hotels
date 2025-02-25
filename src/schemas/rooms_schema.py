from pydantic import BaseModel, Field, ConfigDict


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    cost: int
    quantity: int
    description: str | None = Field(None)


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPATCH(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    cost: int | None = Field(None)
    quantity: int | None = Field(None)
