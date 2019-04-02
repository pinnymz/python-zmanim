from typing import Optional

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.cycle import Cycle
from zmanim.limudim.interval import Interval
from zmanim.limudim.unit import Unit


class Limud:
    def __init__(self, interval: Interval, unit: Optional[Unit]):
        self.__interval = interval
        self.__unit = unit

    @property
    def interval(self) -> Interval:
        return self.__interval

    @property
    def unit(self) -> Optional[Unit]:
        return self.__unit

    def clear(self):
        self.__unit = None

    def cycle(self) -> Cycle:
        return self.interval.cycle

    def description(self) -> str:
        return str(self.unit) if self.unit is not None else ''

    def start_date(self) -> JewishDate:
        return self.interval.start_date

    def end_date(self) -> JewishDate:
        return self.interval.end_date

    def iteration(self) -> int:
        return self.interval.iteration

    def cycle_start_date(self) -> JewishDate:
        return self.cycle().start_date

    def cycle_end_date(self) -> JewishDate:
        return self.cycle().end_date

    def cycle_iteration(self) -> Optional[int]:
        return self.cycle().iteration
