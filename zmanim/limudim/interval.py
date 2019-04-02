from typing import Callable, Optional

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.cycle import Cycle


class Interval:
    def __init__(self, start_date: JewishDate, end_date: JewishDate, iteration: int, cycle: Cycle):
        self.__start_date = start_date
        self.__end_date = end_date
        self.__iteration = iteration
        self.__cycle = cycle

    @property
    def start_date(self) -> JewishDate:
        return self.__start_date

    @property
    def end_date(self) -> JewishDate:
        return self.__end_date

    @property
    def iteration(self) -> int:
        return self.__iteration

    @property
    def cycle(self) -> Cycle:
        return self.__cycle

    @staticmethod
    def first_for_cycle(cycle: Cycle, interval_end_calculation: Callable[[Cycle, JewishDate], JewishDate]) -> 'Interval':
        start_date = cycle.start_date
        iteration = 1
        end_date = interval_end_calculation(cycle, start_date)
        return Interval(start_date, end_date, iteration, cycle)

    def next(self, interval_end_calculation: Callable[[Cycle, JewishDate], JewishDate]) -> Optional['Interval']:
        return self._next_for_iteration(self.iteration+1, interval_end_calculation)

    def skip(self, interval_end_calculation: Callable[[Cycle, JewishDate], JewishDate]) -> Optional['Interval']:
        return self._next_for_iteration(self.iteration, interval_end_calculation)

    def _next_for_iteration(self, new_iteration: int, interval_end_calculation: Callable[[Cycle, JewishDate], JewishDate]) -> Optional['Interval']:
        if self.end_date >= self.cycle.end_date:    # paranoid check to remain in cycle bounds
            return None
        new_start_date = self.end_date + 1
        new_end_date = interval_end_calculation(self.cycle, new_start_date)
        return Interval(new_start_date, new_end_date, new_iteration, self.cycle)
