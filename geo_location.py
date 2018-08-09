import pytz
from numbers import Number
from datetime import datetime


class GeoLocation:
    MINUTE_MILLIS = 60 * 1000
    HOUR_MILLIS = MINUTE_MILLIS * 60

    def __init__(self, name: str, latitude: Number, longitude: Number, time_zone, elevation: Number = None):
        self.location_name = name
        self.latitude = latitude
        self.longitude = longitude
        self.time_zone = time_zone
        self.elevation = elevation

    @property
    def latitude(self) -> Number:
        return self.__latitude

    @latitude.setter
    def latitude(self, latitude):
        if isinstance(latitude, Number):
            if latitude > 90 or latitude < -90:
                raise ValueError("latitude must be in the range -90..90")
            self.__latitude = latitude
        elif isinstance(latitude, (list,tuple)) and len(latitude) == 4:
            degrees, minutes, seconds, direction = latitude[0], latitude[1], latitude[2], latitude[3]
            temp = degrees + ((minutes + (seconds / 60.0)) / 60.0)
            if temp < 0:
                raise ValueError("latitude as cartography must be positive")
            if direction == 'S':
                temp *= -1
            elif direction != 'N':
                raise ValueError("direction must be either 'N' or 'S'")
            self.__latitude = temp
        else:
            raise TypeError("input must be a number or a list in the format 'degrees,minutes,seconds,direction'")

    @property
    def longitude(self) -> Number:
        return self.__longitude

    @longitude.setter
    def longitude(self, longitude):
        if isinstance(longitude, Number):
            if longitude > 180 or longitude < -180:
                raise ValueError("longitude must be in the range -180..180")
            self.__longitude = longitude
        elif isinstance(longitude, (list,tuple)) and len(longitude) == 4:
            degrees, minutes, seconds, direction = longitude[0], longitude[1], longitude[2], longitude[3]
            temp = degrees + ((minutes + (seconds / 60.0)) / 60.0)
            if temp < 0:
                raise ValueError("longitude as cartography must be positive")
            if direction == 'W':
                temp *= -1
            elif direction != 'E':
                raise ValueError("direction must be either 'E' or 'W'")
            self.__longitude = temp
        else:
            raise TypeError("input must be a number or a list in the format 'degrees,minutes,seconds,direction'")

    @property
    def time_zone(self) -> pytz.BaseTzInfo:
        return self.__time_zone

    @time_zone.setter
    def time_zone(self, time_zone):
        if isinstance(time_zone, str):
            self.time_zone = pytz.timezone(time_zone)
        elif isinstance(time_zone, pytz.BaseTzInfo):
            self.__time_zone = time_zone
        else:
            raise TypeError("input must be a timezone or string")

    @property
    def elevation(self) -> Number:
        return self.__elevation

    @elevation.setter
    def elevation(self, elevation):
        if elevation is None:
            elevation = 0
        if elevation < 0:
            raise ValueError("elevation cannot be negative")
        self.__elevation = elevation

    @classmethod
    def GMT(cls):
        return cls('Greenwich, England', 51.4772, 0, 'GMT')

    def antimeridian_adjustment(self) -> int:
        local_hours_offset = self.local_mean_time_offset() / float(self.HOUR_MILLIS)
        if local_hours_offset >= 20:
            return 1
        elif local_hours_offset <= -20:
            return -1
        else:
            return 0

    def local_mean_time_offset(self) -> float:
        return (self.longitude * 4 * self.MINUTE_MILLIS) - self.standard_time_offset()

    def standard_time_offset(self) -> int:
        now = datetime.now(tz=self.time_zone)
        return int((now.utcoffset() - now.dst()).total_seconds()) * 1000

    def time_zone_offset_at(self, utc_time) -> float:
        return utc_time.astimezone(self.time_zone).utcoffset().total_seconds() / 3600.0
