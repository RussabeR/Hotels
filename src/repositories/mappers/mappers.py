from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsORrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.facilities_schema import Facility
from src.schemas.hotels_schema import Hotel
from src.schemas.rooms_schema import Room, RoomWithRels
from src.schemas.users_schema import User, UserWithHashedPassword
from src.schemas.bookings_schema import Booking


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsORrm
    schema = Room


class RoomDataMapperRels(DataMapper):
    db_model = RoomsORrm
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class UserDataMapperHashedPass(DataMapper):
    db_model = UsersOrm
    schema = UserWithHashedPassword


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility
