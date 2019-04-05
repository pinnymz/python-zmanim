from datetime import date

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.cycle import Cycle
from zmanim.limudim.limud_calculator import LimudCalculator


class DafYomiBavli(LimudCalculator):
    Units = {'berachos': 64, 'shabbos': 157, 'eruvin': 105, 'pesachim': 121, 'shekalim': 22, 'yoma': 88, 'sukkah': 56, 'beitzah': 40, 'rosh_hashanah': 35,
             'taanis': 31, 'megillah': 32, 'moed_katan': 29, 'chagigah': 27, 'yevamos': 122, 'kesubos': 112, 'nedarim': 91, 'nazir': 66, 'sotah': 49,
             'gitin': 90, 'kiddushin': 82, 'bava_kamma': 119, 'bava_metzia': 119, 'bava_basra': 176, 'sanhedrin': 113, 'makkos': 24, 'shevuos': 49,
             'avodah_zarah': 76, 'horiyos': 14, 'zevachim': 120, 'menachos': 110, 'chullin': 142, 'bechoros': 61, 'arachin': 34, 'temurah': 34,
             'kerisos': 28, 'meilah': 22, 'kinnim': 25, 'tamid': 33, 'midos': 37, 'niddah': 73}

    def initial_cycle_date(self) -> JewishDate:
        return self._jewish_date(date(1923, 9, 11))

    @staticmethod
    def default_starting_page():
        return 2

    def starting_page(self, units: dict, unit_name: str) -> int:
        if unit_name == 'kinnim':
            return 23
        elif unit_name == 'tamid':
            return 26
        elif unit_name == 'midos':
            return 34
        else:
            return self.default_starting_page()

    @staticmethod
    def default_units() -> dict:
        return DafYomiBavli.Units

    def cycle_end_calculation(self, start_date: JewishDate, iteration: int) -> JewishDate:
        duration = 2702 if iteration < 8 else 2711
        return start_date + (duration - 1)

    def cycle_units_calculation(self, cycle: Cycle) -> dict:
        units = self.default_units().copy()
        if cycle.iteration < 8:
            units['shekalim'] = 13
        return units
