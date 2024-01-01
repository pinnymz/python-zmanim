import math
from datetime import date
from typing import Optional
from abc import ABC, abstractmethod

from zmanim.util.geo_location import GeoLocation



class AstronomicalCalculations(ABC):
    GEOMETRIC_ZENITH = 90.0

    def __init__(self):
        self.refraction = 34 / 60.0
        self.solar_radius = 16 / 60.0
        self.earth_radius = 6356.9  # km

    def elevation_adjustment(self, elevation: float) -> float:
        return math.degrees(math.acos(self.earth_radius / (self.earth_radius + (elevation / 1000.0))))

    def adjusted_zenith(self, zenith: float, elevation: float) -> float:
        if zenith != self.GEOMETRIC_ZENITH:
            return zenith
        return zenith + self.solar_radius + self.refraction + self.elevation_adjustment(elevation)
    
    @abstractmethod
    def utc_sunrise(self, target_date: date, geo_location: GeoLocation, zenith: float, adjust_for_elevation: bool = False) -> Optional[float]:
        pass
    
    @abstractmethod
    def utc_sunset(self, target_date: date, geo_location: GeoLocation, zenith: float, adjust_for_elevation: bool = False) -> Optional[float]:
        pass