from itertools import zip_longest
from math import ceil
from typing import Optional

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.anchor import Anchor
from zmanim.limudim.anchors.day_of_year_anchor import DayOfYearAnchor
from zmanim.limudim.cycle import Cycle
from zmanim.limudim.interval import Interval
from zmanim.limudim.limud_calculator import LimudCalculator


class PirkeiAvos(LimudCalculator):
    def __init__(self, in_israel: bool = False):
        self.__in_israel = in_israel

    @property
    def in_israel(self) -> bool:
        return self.__in_israel

    def is_tiered_units(self) -> bool:
        return False

    def perpetual_cycle_anchor(self) -> Anchor:
        return DayOfYearAnchor(1, 22 if self.in_israel else 23)     # Day after Pesach

    @staticmethod
    def default_units() -> list:
        # 4 sub-cycles of 6 perakim, with the last sub-cycle being compressed as needed
        basic_units = list(range(1, 7))
        return basic_units * 4

    def cycle_end_calculation(self, start_date: JewishDate, iteration: Optional[int]) -> JewishDate:
        rosh_hashana = JewishDate(start_date.jewish_year + 1, 7, 1)
        return rosh_hashana - rosh_hashana.day_of_week   # last Shabbos before Rosh Hashanah

    def interval_end_calculation(self, cycle: Cycle, start_date: JewishDate) -> JewishDate:
        return start_date + (7 - start_date.day_of_week)

    def is_skip_interval(self, interval: Interval) -> bool:
        return (not self.in_israel) and [interval.end_date.jewish_month, interval.end_date.jewish_day] == [3, 7]

    def cycle_units_calculation(self, cycle: Cycle) -> list:
        base_units = self.default_units()
        cycle_weeks = int(ceil(((cycle.end_date - cycle.start_date).days + 1) / 7.0))
        # If the cycle starts on a Friday, outside of israel the 2nd day of Shavuos will fall on Shabbos
        # and we lose one week in the pirkei avos cycle
        if (not self.in_israel) and cycle.start_date.day_of_week == 6:
            cycle_weeks -= 1
        unit_count = len(base_units)
        compress_weeks = (unit_count - cycle_weeks) * 2
        return base_units[:unit_count - compress_weeks] + \
            list(self._each_slice(base_units[-compress_weeks:] if compress_weeks > 0 else [], 2))

    @staticmethod
    def _each_slice(iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)
