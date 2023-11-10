from datetime import date
from fractions import Fraction
from typing import Optional, Union

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.calculators.daf_yomi_bavli import DafYomiBavli
from zmanim.limudim.cycle import Cycle


class AmudYomiBavliDirshu(DafYomiBavli):
    Units = {u[0]: u[1] + (0 if i in [0, 2, 5, 8, 9, 10, 11, 12, 21, 27, 29, 30, 31, 32, 33, 35, 36, 39]
                           else Fraction(1, 2))
             for i, u in enumerate(DafYomiBavli.Units.items())}

    def initial_cycle_date(self) -> JewishDate:
        return self._jewish_date(date(2023, 10, 16))

    @staticmethod
    def default_units() -> dict:
        return AmudYomiBavliDirshu.Units

    def unit_step(self) -> Union[int, Fraction]:
        return Fraction(1, 2)   # Rational numbers preferred over float

    def fractional_units(self) -> Optional[tuple]:
        return 'a', 'b'

    def starting_page(self, units: dict, unit_name: str) -> int:
        if unit_name == 'kinnim':
            return 22 + self.unit_step()
        elif unit_name == 'tamid':
            return 25 + self.unit_step()
        elif unit_name == 'midos':
            return 34
        else:
            return self.default_starting_page()

    def cycle_end_calculation(self, start_date: JewishDate, iteration: int) -> JewishDate:
        return start_date + (5406 - 1)

    def cycle_units_calculation(self, cycle: Cycle) -> dict:
        return self.default_units()
