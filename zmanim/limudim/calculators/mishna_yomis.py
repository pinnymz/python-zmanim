from datetime import date

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.limud_calculator import LimudCalculator


class MishnaYomis(LimudCalculator):
    Units = {maseches: {i + 1: p for i, p in enumerate(perakim)} for maseches, perakim in
             [('berachos', [5, 8, 6, 7, 5, 8, 5, 8, 5]), ('peah', [6, 8, 8, 11, 8, 11, 8, 9]),
              ('demai', [4, 5, 6, 7, 11, 12, 8]), ('kilayim', [9, 11, 7, 9, 8, 9, 8, 6, 10]),
              ('sheviis', [8, 10, 10, 10, 9, 6, 7, 11, 9, 9]),
              ('terumos', [10, 6, 9, 13, 9, 6, 7, 12, 7, 12, 10]),
              ('maasros', [8, 8, 10, 6, 8]), ('maaser_sheni', [7, 10, 13, 12, 15]),
              ('chalah', [9, 8, 10, 11]), ('orlah', [9, 17, 9]), ('bikurim', [11, 11, 12, 5]),
              ('shabbos',
               [11, 7, 6, 2, 4, 10, 4, 7, 7, 6, 6, 6, 7, 4, 3, 8, 8, 3, 6, 5, 3, 6, 5, 5]),
              ('eruvin', [10, 6, 9, 11, 9, 10, 11, 11, 4, 15]),
              ('pesachim', [7, 8, 8, 9, 10, 6, 13, 8, 11, 9]),
              ('shekalim', [7, 5, 4, 9, 6, 6, 7, 8]), ('yoma', [8, 7, 11, 6, 7, 8, 5, 9]),
              ('sukkah', [11, 9, 15, 10, 8]), ('beitzah', [10, 10, 8, 7, 7]),
              ('rosh_hashanah', [9, 8, 9, 9]), ('taanis', [7, 10, 9, 8]),
              ('megillah', [11, 6, 6, 10]),
              ('moed_katan', [10, 5, 9]), ('chagigah', [8, 7, 8]),
              ('yevamos', [4, 10, 10, 13, 6, 6, 6, 6, 6, 9, 7, 6, 13, 9, 10, 7]),
              ('kesubos', [10, 10, 9, 12, 9, 7, 10, 8, 9, 6, 6, 4, 11]),
              ('nedarim', [4, 5, 11, 8, 6, 10, 9, 7, 10, 8, 12]),
              ('nazir', [7, 10, 7, 7, 7, 11, 4, 2, 5]), ('sotah', [9, 6, 8, 5, 5, 4, 8, 7, 15]),
              ('gitin', [6, 7, 8, 9, 9, 7, 9, 10, 10]),
              ('kiddushin', [10, 10, 13, 14]),
              ('bava_kamma', [4, 6, 11, 9, 7, 6, 7, 7, 12, 10]),
              ('bava_metzia', [8, 11, 12, 12, 11, 8, 11, 9, 13, 6]),
              ('bava_basra', [6, 14, 8, 9, 11, 8, 4, 8, 10, 8]),
              ('sanhedrin', [6, 5, 8, 5, 5, 6, 11, 7, 6, 6, 6]), ('makkos', [10, 8, 16]),
              ('shevuos', [7, 5, 11, 13, 5, 7, 8, 6]),
              ('eduyos', [14, 10, 12, 12, 7, 3, 9, 7]), ('avodah_zarah', [9, 7, 10, 12, 12]),
              ('avos', [18, 16, 18, 22, 23, 11]), ('horiyos', [5, 7, 8]),
              ('zevachim', [4, 5, 6, 6, 8, 7, 6, 12, 7, 8, 8, 6, 8, 10]),
              ('menachos', [4, 5, 7, 5, 9, 7, 6, 7, 9, 9, 9, 5, 11]),
              ('chullin', [7, 10, 7, 7, 5, 7, 6, 6, 8, 4, 2, 5]),
              ('bechoros', [7, 9, 4, 10, 6, 12, 7, 10, 8]),
              ('arachin', [4, 6, 5, 4, 6, 5, 5, 7, 8]), ('temurah', [6, 3, 5, 4, 6, 5, 6]),
              ('kerisos', [7, 6, 10, 3, 8, 9]),
              ('meilah', [4, 9, 8, 6, 5, 6]), ('tamid', [4, 5, 9, 3, 6, 4, 3]),
              ('midos', [9, 6, 8, 7, 4]), ('kinnim', [4, 5, 6]),
              ('keilim',
               [9, 8, 8, 4, 11, 4, 6, 11, 8, 8, 9, 8, 8, 8, 6, 8, 17, 9, 10, 7, 3, 10, 5, 17, 9,
                9, 12, 10, 8, 4]),
              ('ohalos', [8, 7, 7, 3, 7, 7, 6, 6, 16, 7, 9, 8, 6, 7, 10, 5, 5, 10]),
              ('negaim', [6, 5, 8, 11, 5, 8, 5, 10, 3, 10, 12, 7, 12, 13]),
              ('parah', [4, 5, 11, 4, 9, 5, 12, 11, 9, 6, 9, 11]),
              ('taharos', [9, 8, 8, 13, 9, 10, 9, 9, 9, 8]),
              ('mikvaos', [8, 10, 4, 5, 6, 11, 7, 5, 7, 8]),
              ('niddah', [7, 7, 7, 7, 9, 14, 5, 4, 11, 8]),
              ('machshirin', [6, 11, 8, 10, 11, 8]), ('zavim', [6, 4, 3, 7, 12]),
              ('tevul_yom', [5, 8, 6, 7]), ('yadayim', [5, 4, 5, 8]), ('uktzin', [6, 10, 12])]
             }

    def initial_cycle_date(self) -> JewishDate:
        return self._jewish_date(date(1947, 5, 20))

    @staticmethod
    def default_units() -> dict:
        return MishnaYomis.Units

    def cycle_end_calculation(self, start_date: JewishDate, iteration: int) -> JewishDate:
        return start_date + (int(4192/2) - 1)

    def unit_step(self):
        return 2

