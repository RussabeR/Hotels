from pydantic import BaseModel, ConfigDict


class FacilityAdd(BaseModel):
    title: str


class Facility(FacilityAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomFacilityAdd(BaseModel):
    facility_id: int
    room_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
