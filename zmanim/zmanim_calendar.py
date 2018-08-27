from datetime import datetime, timedelta
from typing import Optional

from zmanim.astronomical_calendar import AstronomicalCalendar


class ZmanimCalendar(AstronomicalCalendar):
    def __init__(self, candle_lighting_offset: int = None, *args, **kwargs):
        super(ZmanimCalendar, self).__init__(*args, **kwargs)
        self.candle_lighting_offset = 18 if candle_lighting_offset is None else candle_lighting_offset

    def __repr__(self):
        return "%s(candle_lighting_offset=%r, geo_location=%r, date=%r, calculator=%r)" % \
               (self.__module__ + "." + self.__class__.__qualname__, self.candle_lighting_offset,
                self.geo_location, self.date, self.astronomical_calculator)

    def tzais(self, opts: dict = {'degrees': 8.5}) -> Optional[datetime]:
        degrees, offset = self._extract_degrees_offset(opts)
        return self._offset_by_minutes(self.sunset_offset_by_degrees(self.GEOMETRIC_ZENITH + degrees), offset)

    def tzais_72(self) -> Optional[datetime]:
        return self.tzais({'offset': 72})

    def alos(self, opts: dict = {'degrees': 16.1}) -> Optional[datetime]:
        degrees, offset = self._extract_degrees_offset(opts)
        return self._offset_by_minutes(self.sunrise_offset_by_degrees(self.GEOMETRIC_ZENITH + degrees), offset)

    def alos_72(self) -> Optional[datetime]:
        return self.alos({'offset': -72})

    def chatzos(self) -> Optional[datetime]:
        return self.sun_transit()

    def candle_lighting(self) -> Optional[datetime]:
        return self._offset_by_minutes(self.sea_level_sunset(), -self.candle_lighting_offset)

    def sof_zman_shma(self, day_start: datetime, day_end: datetime) -> datetime:
        return self._shaos_into_day(day_start, day_end, 3)

    def sof_zman_shma_gra(self) -> datetime:
        return self.sof_zman_shma(self.sea_level_sunrise(), self.sea_level_sunset())

    def sof_zman_shma_mga(self) -> datetime:
        return self.sof_zman_shma(self.alos_72(), self.tzais_72())

    def sof_zman_tfila(self, day_start: Optional[datetime], day_end: Optional[datetime]) -> Optional[datetime]:
        return self._shaos_into_day(day_start, day_end, 4)

    def sof_zman_tfila_gra(self) -> Optional[datetime]:
        return self.sof_zman_tfila(self.sea_level_sunrise(), self.sea_level_sunset())

    def sof_zman_tfila_mga(self) -> Optional[datetime]:
        return self.sof_zman_tfila(self.alos_72(), self.tzais_72())

    def mincha_gedola(self, day_start: Optional[datetime] = None, day_end: Optional[datetime] = None) -> Optional[datetime]:
        if day_start is None:
            day_start = self.sea_level_sunrise()
        if day_end is None:
            day_end = self.sea_level_sunset()

        return self._shaos_into_day(day_start, day_end, 6.5)

    def mincha_ketana(self, day_start: Optional[datetime] = None, day_end: Optional[datetime] = None) -> Optional[datetime]:
        if day_start is None:
            day_start = self.sea_level_sunrise()
        if day_end is None:
            day_end = self.sea_level_sunset()

        return self._shaos_into_day(day_start, day_end, 9.5)

    def plag_hamincha(self, day_start: Optional[datetime] = None, day_end: Optional[datetime] = None) -> Optional[datetime]:
        if day_start is None:
            day_start = self.sea_level_sunrise()
        if day_end is None:
            day_end = self.sea_level_sunset()

        return self._shaos_into_day(day_start, day_end, 10.75)

    def shaah_zmanis(self, day_start: Optional[datetime], day_end: Optional[datetime]) -> Optional[float]:
        return self.temporal_hour(day_start, day_end)

    def shaah_zmanis_gra(self) -> Optional[float]:
        return self.shaah_zmanis(self.sea_level_sunrise(), self.sea_level_sunset())

    def shaah_zmanis_mga(self) -> Optional[float]:
        return self.shaah_zmanis(self.alos_72(), self.tzais_72())

    def shaah_zmanis_by_degrees_and_offset(self, degrees: float, offset: float) -> Optional[float]:
        opts = {'degrees': degrees, 'offset': offset}
        return self.shaah_zmanis(self.alos({**opts, 'offset': -offset}), self.tzais(opts))

    def _shaos_into_day(self, day_start: Optional[datetime], day_end: Optional[datetime], shaos: float) -> Optional[datetime]:
        shaah_zmanis = self.temporal_hour(day_start, day_end)
        if shaah_zmanis is None:
            return None
        return self._offset_by_minutes(day_start, (shaah_zmanis / self.MINUTE_MILLIS) * shaos)

    def _extract_degrees_offset(self, opts: dict) -> tuple:
        degrees = opts['degrees'] if 'degrees' in opts else 0
        offset = opts['offset'] if 'offset' in opts else 0
        return degrees, offset

    def _offset_by_minutes(self, time: Optional[datetime], minutes: float) -> Optional[datetime]:
        if time is None:
            return None
        return time + timedelta(minutes=minutes)
