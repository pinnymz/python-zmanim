from datetime import date

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.calculators.daf_yomi_bavli import DafYomiBavli
from zmanim.limudim.cycle import Cycle


class DafHashavuaBavli(DafYomiBavli):
    def initial_cycle_date(self) -> JewishDate:
        return self._jewish_date(date(2005, 3, 2))

    def cycle_end_calculation(self, start_date: JewishDate, iteration: int) -> JewishDate:
        return start_date + ((2711 * 7) - start_date.day_of_week)  # 2711 pages except first week * 7 days

    def interval_end_calculation(self, cycle: Cycle, start_date: JewishDate) -> JewishDate:
        return start_date + (7 - start_date.day_of_week)

    def cycle_units_calculation(self, cycle: Cycle) -> dict:
        return self.default_units()
