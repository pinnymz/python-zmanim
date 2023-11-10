from datetime import date
from fractions import Fraction
from functools import reduce
from numbers import Number
from typing import Optional, Union

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.anchor import Anchor
from zmanim.limudim.cycle import Cycle
from zmanim.limudim.interval import Interval
from zmanim.limudim.limud import Limud
from zmanim.limudim.unit import Unit


class LimudCalculator:
    def limud(self, limud_date: Union[date, JewishDate]) -> Optional[Limud]:
        jewish_date = self._jewish_date(limud_date)
        cycle = self.find_cycle(jewish_date)
        if cycle is None or cycle.end_date < jewish_date:
            return None
        units = self.cycle_units_calculation(cycle)
        interval = Interval.first_for_cycle(cycle, self.interval_end_calculation)
        while not interval.start_date <= jewish_date <= interval.end_date:
            if self.is_skip_interval(interval):
                interval = interval.skip(self.interval_end_calculation)
            else:
                interval = interval.next(self.interval_end_calculation)

        unit = self.unit_for_interval(units, interval)
        return Limud(interval, unit)

    # Jewish Date on which the first cycle starts (if not perpetual)
    def initial_cycle_date(self) -> Optional[JewishDate]:
        return None

    # Anchor on which a cycle resets (where relevant)
    # e.g. for Parsha this would be a Day-of-Year anchor
    def perpetual_cycle_anchor(self) -> Optional[Anchor]:
        return None

    # Number of units to apply over an iteration
    def unit_step(self) -> Union[int, Fraction]:
        return 1

    # Are units components of some larger grouping? (e.g. pages or mishnayos)
    def is_tiered_units(self) -> bool:
        return True

    # For tiered units, this would be a dict in the format:
    #   `{'some_name': last_page, ...}`
    # or:
    #   `{'maseches': {perek_number: mishnayos, ...}, ...}`.
    #
    # For simple units, use a list in the format:
    #   `['some_name', ...]`
    @staticmethod
    def default_units() -> Union[dict, list]:
        return []

    # Set if units are applied fractionally (indicated by a fractional unit_step).
    # For example, an amud yomi calculator would set `('a', 'b')`
    def fractional_units(self) -> Optional[tuple]:
        return None

    # Change this when using page numbers that do not generally start from one.
    # (e.g. Talmud Bavli pages start from 2)
    @staticmethod
    def default_starting_page() -> int:
        return 1

    def starting_page(self, units: Union[dict, list], unit_name: str) -> int:
        return self.default_starting_page()

    def cycle_end_calculation(self, start_date: JewishDate, iteration: Optional[int]) -> JewishDate:
        return start_date

    def interval_end_calculation(self, cycle: Cycle, start_date: JewishDate) -> JewishDate:
        return start_date

    def cycle_units_calculation(self, cycle: Cycle) -> Union[dict, list]:
        return self.default_units()

    def unit_for_interval(self, units: Union[dict, list], interval: Interval) -> Optional[Unit]:
        if self.is_skip_interval(interval):
            return self.skip_unit()
        if self.is_tiered_units():
            return self.tiered_units_for_interval(units, interval)
        if len(units) >= interval.iteration:
            unit = units[interval.iteration-1]
            return Unit(unit) if isinstance(unit, str) or not isinstance(unit, (list, tuple)) else Unit(*unit)
        return None

    def skip_unit(self) -> Optional[Unit]:
        return None

    def is_skip_interval(self, interval: Interval) -> bool:
        return False

    def base_unit(self) -> Union[int, Fraction]:
        return self.unit_step() if self.fractional_units() else 1

    def tiered_units_for_interval(self, units: Union[dict, list], interval: Interval) -> Optional[Unit]:
        iteration = interval.iteration
        offset = ((iteration - 1) * self.unit_step()) + self.base_unit()
        offset2 = (offset - 1) + self.unit_step() if self.unit_step() > 1 else None
        offsets = list(filter(None.__ne__, [offset, offset2]))
        targets = [[o, []] for o in offsets]
        results = self.find_offset_units(units, targets)
        if {r[0] for r in results} != {0}:
            return None
        paths = list(map(lambda r: r[1], results))
        if self.fractional_units():
            paths = list(map(lambda p: self._resolve_fractional_path(p), paths))
        return Unit(*paths)

    def find_offset_units(self, units: Union[dict, list], targets: list) -> list:
        def unit_reducer(t: list, name: str):
            attributes = units[name]
            if isinstance(attributes, (int, Fraction)):
                start = self.starting_page(units, name)
                length = (attributes - start) + self.base_unit()

                head = [e for e in t if e[0] == 0]
                tail = [[0, p + [name, (start + o) - self.base_unit()]] if o <= length else [o - length, p] for o, p in t if o != 0]
                return head + tail
            else:
                head = [e for e in t if e[0] == 0]
                offset_units = self.find_offset_units(attributes, [[o, p + [name]] for o, p in t if o != 0])
                tail = [[o, p] if o == 0 else [o, p[:-1]] for o, p in offset_units]
                return head + tail

        return list(reduce(unit_reducer, units, targets))

    def find_cycle(self, date: JewishDate):
        if self.initial_cycle_date() is not None:
            return Cycle.from_cycle_initiation(self.initial_cycle_date(), self.cycle_end_calculation, date)
        elif self.perpetual_cycle_anchor() is not None:
            return Cycle.from_perpetual_anchor(self.perpetual_cycle_anchor(), self.cycle_end_calculation, date)
        else:
            raise NotImplementedError

    @staticmethod
    def _jewish_date(date):
        return date if isinstance(date, JewishDate) else JewishDate(date)

    def _resolve_fractional_path(self, path: Union[list, Number]) -> Union[list, Number]:
        if isinstance(path, Number):
            index = int((path - int(path)) * len(self.fractional_units()))
            return [int(path), self.fractional_units()[index]]
        elif isinstance(path, list):
            return path[:-1] + self._resolve_fractional_path(path[-1])
        else:
            return path