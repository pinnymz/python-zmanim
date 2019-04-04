from typing import Optional

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.anchor import Anchor
from zmanim.limudim.anchors.day_of_month_anchor import DayOfMonthAnchor
from zmanim.limudim.interval import Interval
from zmanim.limudim.limud_calculator import LimudCalculator
from zmanim.limudim.unit import Unit


class TehillimMonthly(LimudCalculator):
    def is_tiered_units(self) -> bool:
        return False

    def perpetual_cycle_anchor(self) -> Anchor:
        return DayOfMonthAnchor(1)

    @staticmethod
    def default_units() -> list:
        return [9, 17, 22, 28, 34, 38, 43, 48, 54, 59, 65, 68, 71, 76, 78, 82, 87, 89, 96, 103, 105, 107, 112, 118, 119,
                119, 134, 139, 144, 150]

    def cycle_end_calculation(self, start_date: JewishDate, iteration: Optional[int]) -> JewishDate:
        return self.perpetual_cycle_anchor().next_occurrence(start_date) - 1

    def unit_for_interval(self, units: list, interval: Interval) -> Unit:
        if interval.iteration == 1:
            start, stop = [1, units[interval.iteration - 1]]
        elif interval.iteration == 25:
            start, stop = [[119, 1], [119, 30]]
        elif interval.iteration == 26:
            start, stop = [[119, 40], [119, 400]]
        else:
            start, stop = [units[interval.iteration - 2] + 1, units[interval.iteration - 1]]

        if interval.end_date.jewish_day == 29 and interval.end_date.days_in_jewish_month() == 29:
            stop = units[interval.iteration]

        return Unit(start, stop)
