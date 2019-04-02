from typing import Callable, Optional

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.anchor import Anchor


class Cycle:
    def __init__(self, start_date: JewishDate, end_date: JewishDate, iteration: Optional[int]):
        self.__start_date = start_date
        self.__end_date = end_date
        self.__iteration = iteration

    @property
    def start_date(self) -> JewishDate:
        return self.__start_date

    @property
    def end_date(self) -> JewishDate:
        return self.__end_date

    @property
    def iteration(self) -> Optional[int]:
        return self.__iteration

    @staticmethod
    def from_perpetual_anchor(anchor: Anchor, cycle_end_calculation: Callable[[JewishDate, Optional[int]], JewishDate], date: JewishDate) -> 'Cycle':
        start_date = anchor.current_or_previous_occurrence(date)
        end_date = cycle_end_calculation(start_date, None)
        return Cycle(start_date, end_date, None)

    @staticmethod
    def from_cycle_initiation(initial_cycle_date: JewishDate, cycle_end_calculation: Callable[[JewishDate, Optional[int]], JewishDate], date: JewishDate) -> Optional['Cycle']:
        if initial_cycle_date > date:
            return None
        iteration = 1
        end_date = cycle_end_calculation(initial_cycle_date, iteration)
        cycle = Cycle(initial_cycle_date, end_date, iteration)
        while date > cycle.end_date:
            cycle = cycle.next(cycle_end_calculation)
        return cycle

    def next(self, cycle_end_calculation: Callable[[JewishDate, Optional[int]], JewishDate]) -> Optional['Cycle']:
        if self.iteration is None:
            return None
        new_iteration = self.iteration + 1
        new_start_date = self.end_date + 1
        new_end_date = cycle_end_calculation(new_start_date, new_iteration)
        return Cycle(new_start_date, new_end_date, new_iteration)
