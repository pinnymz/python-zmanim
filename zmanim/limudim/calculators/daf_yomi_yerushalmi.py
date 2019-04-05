from datetime import date

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.interval import Interval
from zmanim.limudim.limud_calculator import LimudCalculator
from zmanim.limudim.unit import Unit


class DafYomiYerushalmi(LimudCalculator):
    Units = {'berachos': 68, 'peah': 37, 'demai': 34, 'kilayim': 44, 'shviis': 31, 'terumos': 59, 'maasros': 26, 'maaser_sheni': 33,
             'chalah': 28, 'orlah': 20, 'bikurim': 13, 'shabbos': 92, 'eruvin': 65, 'pesachim': 71, 'beitzah': 22, 'rosh_hashanah': 22,
             'yoma': 42, 'sukkah': 26, 'taanis': 26, 'shekalim': 33, 'megilah': 34, 'chagigah': 22, 'moed_katan': 19, 'yevamos': 85,
             'kesubos': 72, 'sotah': 47, 'nedarim': 40, 'nazir': 47, 'gitin': 54, 'kiddushin': 48, 'bava_kama': 44, 'bava_metzia': 37,
             'bava_basra': 34, 'sanhedrin': 44, 'makos': 9, 'shevuos': 57, 'avodah_zarah': 37, 'horayos': 19, 'niddah': 13}

    def initial_cycle_date(self) -> JewishDate:
        return self._jewish_date(date(1980, 2, 2))

    @staticmethod
    def default_units() -> dict:
        return DafYomiYerushalmi.Units

    def cycle_end_calculation(self, start_date: JewishDate, iteration: int) -> JewishDate:
        def found_skips_for_year(year, a, b):
            return len([(m, d) for m, d in self._skip_days() if a <= JewishDate(year, m, d) <= b])

        def found_skips_between(a, b):
            return sum([found_skips_for_year(year, a, b) for year in range(a.jewish_year, b.jewish_year + 1)])

        end_date = start_date + (1554 - 1)
        found_days = found_skips_between(start_date, end_date)
        while found_days > 0:
            start_date, end_date = end_date + 1, end_date + found_days
            found_days = found_skips_between(start_date, end_date)

        return end_date

    def skip_unit(self):
        return Unit('no_daf_today')

    def is_skip_interval(self, interval: Interval) -> bool:
        return self._matches_skip_day(interval.start_date)

    def _matches_skip_day(self, date: JewishDate) -> bool:
        return any(date.jewish_month == m and date.jewish_day == d for m, d in self._skip_days())

    def _skip_days(self) -> list:
        return [(5, 9), (7, 10)]
