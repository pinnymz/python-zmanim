import math
from datetime import date, datetime, time
from typing import Optional

import julian

from zmanim.util.astronomical_calculations import AstronomicalCalculations
from zmanim.util.geo_location import GeoLocation


class NOAACalculator(AstronomicalCalculations):
    JULIAN_DAY_JAN_1_2000 = 2451545.0
    JULIAN_DAYS_PER_CENTURY = 36525.0

    @staticmethod
    def name():
        return 'US National Oceanic and Atmospheric Administration Algorithm'

    def utc_sunrise(self, target_date: date, geo_location: GeoLocation, zenith: float, adjust_for_elevation: bool = False) -> Optional[float]:
        try:
            return self._utc_sun_position(target_date, geo_location, zenith, adjust_for_elevation, 'sunrise')
        except ValueError:
            return None

    def utc_sunset(self, target_date: date, geo_location: GeoLocation, zenith: float, adjust_for_elevation: bool = False) -> Optional[float]:
        try:
            return self._utc_sun_position(target_date, geo_location, zenith, adjust_for_elevation, 'sunset')
        except ValueError:
            return None

    def _julian_centuries_from_julian_day(self, julian_day: float) -> float:
        return (julian_day - self.JULIAN_DAY_JAN_1_2000) / self.JULIAN_DAYS_PER_CENTURY

    def _julian_day_from_julian_centuries(self, julian_centuries: float) -> float:
        return (julian_centuries * self.JULIAN_DAYS_PER_CENTURY) + self.JULIAN_DAY_JAN_1_2000

    def _utc_sun_position(self, target_date: date, geo_location: GeoLocation, zenith: float, adjust_for_elevation: bool, mode: str) -> float:
        if not isinstance(target_date, datetime):
            target_date = datetime.combine(target_date, time())
        elevation = geo_location.elevation if adjust_for_elevation else 0.0
        adjusted_zenith = self.adjusted_zenith(zenith, elevation)
        utc_time = self._calculate_utc_sun_position(julian.to_jd(target_date),
                                                    geo_location.latitude,
                                                    -geo_location.longitude,
                                                    adjusted_zenith,
                                                    mode)  # in minutes
        utc_time /= 60.0  # in hours
        return utc_time % 24  # normalized (0...24)

    def _calculate_utc_sun_position(self, julian_day: float, latitude: float, longitude: float, zenith: float, mode: str) -> float:
        julian_centuries = self._julian_centuries_from_julian_day(julian_day)

        # first pass using solar noon
        noonmin = self._solar_noon_utc(julian_centuries, longitude)
        tnoon = self._julian_centuries_from_julian_day(julian_day + (noonmin / 1440.0))
        first_pass = self._approximate_utc_sun_position(tnoon, latitude, longitude, zenith, mode)

        # refine using output of first pass
        trefinement = self._julian_centuries_from_julian_day(julian_day + (first_pass / 1440.0))
        return self._approximate_utc_sun_position(trefinement, latitude, longitude, zenith, mode)

    def _approximate_utc_sun_position(self, approx_julian_centuries: float, latitude: float, longitude: float, zenith: float, mode: str) -> float:
        eq_time = self._equation_of_time(approx_julian_centuries)
        solar_dec = self._solar_declination(approx_julian_centuries)
        hour_angle = self._sun_hour_angle_at_horizon(latitude, solar_dec, zenith, mode)

        delta = longitude - math.degrees(hour_angle)
        time_delta = delta * 4.0
        return 720 + time_delta - eq_time

    def _sun_hour_angle_at_horizon(self, latitude: float, solar_dec: float, zenith: float, mode: str) -> float:
        lat_r = math.radians(latitude)
        solar_dec_r = math.radians(solar_dec)
        zenith_r = math.radians(zenith)

        hour_angle = math.acos(
            (math.cos(zenith_r) / (math.cos(lat_r) * math.cos(solar_dec_r))) -
            (math.tan(lat_r) * math.tan(solar_dec_r))
        )

        if mode == 'sunset':
            hour_angle *= -1

        return hour_angle  # in radians

    def _solar_declination(self, julian_centuries: float) -> float:
        correction = math.radians(self._obliquity_correction(julian_centuries))
        apparent_longitude = math.radians(self._sun_apparent_longitude(julian_centuries))
        sint = math.sin(correction) * math.sin(apparent_longitude)
        return math.degrees(math.asin(sint))  # in degrees

    def _sun_apparent_longitude(self, julian_centuries: float) -> float:
        true_longitude = self._sun_true_longitude(julian_centuries)
        omega = 125.04 - (1934.136 * julian_centuries)
        return true_longitude - 0.00569 - (0.00478 * math.sin(math.radians(omega)))  # in degrees

    def _sun_true_longitude(self, julian_centuries: float) -> float:
        sgml = self._sun_geometric_mean_longitude(julian_centuries)
        center = self._sun_equation_of_center(julian_centuries)
        return sgml + center  # in degrees

    def _sun_equation_of_center(self, julian_centuries: float) -> float:
        mrad = math.radians(self._sun_geometric_mean_anomaly(julian_centuries))
        sinm = math.sin(mrad)
        sin2m = math.sin(2 * mrad)
        sin3m = math.sin(3 * mrad)

        return (sinm * (1.914602 - (julian_centuries * (0.004817 + (0.000014 * julian_centuries))))) + \
               (sin2m * (0.019993 - (0.000101 * julian_centuries))) + \
               (sin3m * 0.000289)  # in degrees

    def _solar_noon_utc(self, julian_centuries: float, longitude: float) -> float:
        century_start = self._julian_day_from_julian_centuries(julian_centuries)

        # first pass to yield approximate solar noon
        approx_tnoon = self._julian_centuries_from_julian_day(century_start + (longitude / 360.0))
        approx_eq_time = self._equation_of_time(approx_tnoon)
        approx_sol_noon = 720 + (longitude * 4) - approx_eq_time

        # refinement using output of first pass
        tnoon = self._julian_centuries_from_julian_day(century_start - 0.5 + (approx_sol_noon / 1440.0))
        eq_time = self._equation_of_time(tnoon)
        return 720 + (longitude * 4) - eq_time

    def _equation_of_time(self, julian_centuries: float) -> float:
        epsilon = math.radians(self._obliquity_correction(julian_centuries))
        sgml = math.radians(self._sun_geometric_mean_longitude(julian_centuries))
        sgma = math.radians(self._sun_geometric_mean_anomaly(julian_centuries))
        eoe = self._earth_orbit_eccentricity(julian_centuries)

        y = math.tan(epsilon / 2.0)
        y *= y

        sin2l0 = math.sin(2.0 * sgml)
        sin4l0 = math.sin(4.0 * sgml)
        cos2l0 = math.cos(2.0 * sgml)
        sinm = math.sin(sgma)
        sin2m = math.sin(2.0 * sgma)

        eq_time = (y * sin2l0) - (2.0 * eoe * sinm) + (4.0 * eoe * y * sinm * cos2l0) - (0.5 * y * y * sin4l0) - \
                  (1.25 * eoe * eoe * sin2m)
        return math.degrees(eq_time) * 4.0  # minutes of time

    def _earth_orbit_eccentricity(self, julian_centuries: float) -> float:
        return 0.016708634 - (julian_centuries * (0.000042037 + (0.0000001267 * julian_centuries)))  # unitless

    def _sun_geometric_mean_anomaly(self, julian_centuries: float) -> float:
        anomaly = 357.52911 + (julian_centuries * (35999.05029 - (0.0001537 * julian_centuries)))  # in degrees

        return anomaly % 360  # normalized (0...360)

    def _sun_geometric_mean_longitude(self, julian_centuries: float) -> float:
        longitude = 280.46646 + (julian_centuries * (36000.76983 + (0.0003032 * julian_centuries)))  # in degrees

        return longitude % 360  # normalized (0...360)

    def _obliquity_correction(self, julian_centuries: float) -> float:
        obliquity_of_ecliptic = self._mean_obliquity_of_ecliptic(julian_centuries)

        omega = 125.04 - (1934.136 * julian_centuries)
        correction = obliquity_of_ecliptic + (0.00256 * math.cos(math.radians(omega)))
        return correction % 360  # normalized (0...360)

    def _mean_obliquity_of_ecliptic(self, julian_centuries: float) -> float:
        seconds = 21.448 - (
                    julian_centuries * (46.8150 + (julian_centuries * (0.00059 - (julian_centuries * 0.001813)))))
        return 23.0 + ((26.0 + (seconds / 60)) / 60.0)  # in degrees
