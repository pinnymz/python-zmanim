from functools import reduce
from typing import Optional

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.anchor import Anchor
from zmanim.limudim.anchors.day_of_year_anchor import DayOfYearAnchor
from zmanim.limudim.cycle import Cycle
from zmanim.limudim.limud_calculator import LimudCalculator


class Parsha(LimudCalculator):
    Units = ['bereishis', 'noach', 'lech_lecha', 'vayeira', 'chayei_sarah', 'toldos', 'vayeitzei', 'vayishlach', 'vayeishev', 'mikeitz', 'vayigash', 'vayechi',
             'shemos', 'vaeirah', 'bo', 'beshalach', 'yisro', 'mishpatim', 'terumah', 'tetzaveh', 'ki_sisa', 'vayakheil', 'pekudei',
             'vayikra', 'tzav', 'shemini', 'tazria', 'metzora', 'acharei', 'kedoshim', 'emor', 'behar', 'bechukosai',
             'bamidbar', 'naso', 'behaalosecha', 'shelach', 'korach', 'chukas', 'balak', 'pinchas', 'matos', 'masei',
             'devarim', 'vaeschanan', 'eikev', 'reei', 'shoftim', 'ki_seitzei', 'ki_savo', 'nitzavim', 'vayeilech', 'haazinu', 'vezos_haberacha']

    Kviah = JewishDate.CHESHVAN_KISLEV_KEVIAH
    IsraelModifications = {
                (2, Kviah.chaseirim, 5): [['matos', 'masei'], ['nitzavim', 'vayeilech']],
                (2, Kviah.shelaimim, 7): [],
                (3, Kviah.kesidran, 7): [],
                (5, Kviah.chaseirim, 1): [],
                (5, Kviah.shelaimim, 3): [['nitzavim', 'vayeilech']],
                (7, Kviah.chaseirim, 3): [['matos', 'masei'], ['nitzavim', 'vayeilech']],
                (7, Kviah.shelaimim, 5): [['matos', 'masei'], ['nitzavim', 'vayeilech']],
                (2, Kviah.chaseirim, 3): [['vayakheil', 'pikudei'], ['tazria', 'metzora'], ['acharei', 'kedoshim'],
                                          ['behar', 'bechukosai'], ['matos', 'masei'], ['nitzavim', 'vayeilech']],
                (2, Kviah.shelaimim, 5): [['vayakheil', 'pikudei'], ['tazria', 'metzora'], ['acharei', 'kedoshim'],
                                          ['behar', 'bechukosai'], ['matos', 'masei'], ['nitzavim', 'vayeilech']],
                (3, Kviah.kesidran, 5): [['vayakheil', 'pikudei'], ['tazria', 'metzora'], ['acharei', 'kedoshim'],
                                         ['behar', 'bechukosai'], ['matos', 'masei'], ['nitzavim', 'vayeilech']],
                (5, Kviah.kesidran, 7): [['vayakheil', 'pikudei'], ['tazria', 'metzora'], ['acharei', 'kedoshim'],
                                         ['matos', 'masei']],
                (5, Kviah.shelaimim, 1): [['tazria', 'metzora'], ['acharei', 'kedoshim'], ['behar', 'bechukosai'],
                                          ['matos', 'masei']],
                (7, Kviah.chaseirim, 1): [['vayakheil', 'pikudei'], ['tazria', 'metzora'], ['acharei', 'kedoshim'],
                                          ['behar', 'bechukosai'], ['matos', 'masei']],
                (7, Kviah.shelaimim, 3): [['vayakheil', 'pikudei'], ['tazria', 'metzora'], ['acharei', 'kedoshim'],
                                          ['behar', 'bechukosai'], ['matos', 'masei']],
            }

    DiasporaModifications = {
                (2, Kviah.chaseirim, 5): [['chukas', 'balak'], ['matos', 'masei'], ['nitzavim', 'vayeilech']],
                (2, Kviah.shelaimim, 7): [['matos', 'masei']],
                (3, Kviah.kesidran, 7): [['matos', 'masei']],
                (5, Kviah.chaseirim, 1): [],
                (5, Kviah.shelaimim, 3): [['nitzavim', 'vayeilech']],
                (7, Kviah.chaseirim, 3): [['matos', 'masei'], ['nitzavim', 'vayeilech']],
                (7, Kviah.shelaimim, 5): [['chukas', 'balak'], ['matos', 'masei'], ['nitzavim', 'vayeilech']],
                (2, Kviah.chaseirim, 3): [['vayakheil', 'pikudei'], ['tazria', 'metzora'], ['acharei', 'kedoshim'],
                                          ['behar', 'bechukosai'], ['matos', 'masei'], ['nitzavim', 'vayeilech']],
                (2, Kviah.shelaimim, 5): [['vayakheil', 'pikudei'], ['tazria', 'metzora'], ['acharei', 'kedoshim'],
                                          ['behar', 'bechukosai'], ['chukas', 'balak'], ['matos', 'masei'],
                                          ['nitzavim', 'vayeilech']],
                (3, Kviah.kesidran, 5): [['vayakheil', 'pikudei'], ['tazria', 'metzora'], ['acharei', 'kedoshim'],
                                         ['behar', 'bechukosai'], ['chukas', 'balak'], ['matos', 'masei'],
                                         ['nitzavim', 'vayeilech']],
                (5, Kviah.kesidran, 7): [['vayakheil', 'pikudei'], ['tazria', 'metzora'], ['acharei', 'kedoshim'],
                                         ['behar', 'bechukosai'], ['matos', 'masei']],
                (5, Kviah.shelaimim, 1): [['tazria', 'metzora'], ['acharei', 'kedoshim'], ['behar', 'bechukosai'],
                                          ['matos', 'masei']],
                (7, Kviah.chaseirim, 1): [['vayakheil', 'pikudei'], ['tazria', 'metzora'], ['acharei', 'kedoshim'],
                                          ['behar', 'bechukosai'], ['matos', 'masei']],
                (7, Kviah.shelaimim, 3): [['vayakheil', 'pikudei'], ['tazria', 'metzora'], ['acharei', 'kedoshim'],
                                          ['behar', 'bechukosai'], ['matos', 'masei'], ['nitzavim', 'vayeilech']],
            }

    def __init__(self, in_israel: bool = False):
        self.__in_israel = in_israel

    @property
    def in_israel(self) -> bool:
        return self.__in_israel

    def is_tiered_units(self) -> bool:
        return False

    def perpetual_cycle_anchor(self) -> Anchor:
        return DayOfYearAnchor(7, 23 if self.in_israel else 24)

    @staticmethod
    def default_units() -> list:
        return Parsha.Units

    def cycle_end_calculation(self, start_date: JewishDate, iteration: Optional[int]) -> JewishDate:
        return self.perpetual_cycle_anchor().next_occurrence(start_date) - 1

    def interval_end_calculation(self, cycle: Cycle, start_date: JewishDate) -> JewishDate:
        if self.in_israel:
            skips = [[1, range(15,22)], [3, [6]], [7, [1, 2, 10] + list(range(15,22))]]
        else:
            skips = [[1, range(15,23)], [3, [6, 7]], [7, [1, 2, 10] + list(range(15,23))]]

        end_date = start_date + (7 - start_date.day_of_week)

        while next(((month, days) for month, days in skips if month == end_date.jewish_month and end_date.jewish_day in days), None) is not None:
            end_date += 7

        return cycle.end_date if end_date > cycle.end_date else end_date

    def cycle_units_calculation(self, cycle: Cycle) -> list:
        kviah_values = cycle.start_date.kviah()
        if self.in_israel:
            modifications = Parsha.IsraelModifications[kviah_values]
        else:
            modifications = Parsha.DiasporaModifications[kviah_values]

        def modification_reducer(transitioned_units, parsha_pair):
            index = transitioned_units.index(parsha_pair[0])
            return transitioned_units[0:index] + [parsha_pair] + transitioned_units[index+2:]

        return reduce(modification_reducer, modifications, self.default_units().copy())
