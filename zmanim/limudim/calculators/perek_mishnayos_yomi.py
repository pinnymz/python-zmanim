from datetime import date

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.calculators.mishna_yomis import MishnaYomis


class PerekMishnayosYomi(MishnaYomis):
    PerekUnits = {maseches: len(perakim) for maseches, perakim in MishnaYomis.Units.items()}

    @staticmethod
    def default_units() -> dict:
        return PerekMishnayosYomi.PerekUnits

    def initial_cycle_date(self) -> JewishDate:
        return self._jewish_date(date(1947, 5, 20))  # your start date here

    def cycle_end_calculation(self, start_date: JewishDate, iteration: int) -> JewishDate:
        return start_date + (525 - 1)

    def unit_step(self) -> int:
        return 1