from functools import reduce
from typing import Optional, Union

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.anchor import Anchor
from zmanim.limudim.cycle import Cycle
from zmanim.limudim.interval import Interval
from zmanim.limudim.limud import Limud
from zmanim.limudim.unit import Unit


class LimudCalculator:
    def limud(self, date: JewishDate) -> Optional[Limud]:
        jewish_date = self._jewish_date(date)
        cycle = self.find_cycle(jewish_date)
        if cycle is None or cycle.end_date < date:
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
    def unit_step(self) -> int:
        return 1

    # Are units components of some larger grouping? (e.g. pages or mishnayos)
    def is_tiered_units(self) -> bool:
        return True

    # For tiered units, this would be a Hash in the format:
    #   `{some_name: last_page, ...}`
    # or:
    #   `{maseches: {perek_number => mishnayos, ...}, ...}`.
    #
    # For simple units, use an Array in the format:
    #   `['some_name', ...]`
    def default_units(self) -> Union[dict, list]:
        return {}

    # Set if units are applied fractionally (indicated by a fractional unit_step).
    # For example, an amud yomi calculator would set `('a', 'b')`
    def fractional_units(self) -> Optional[tuple]:
        return None

    # Change this when using page numbers that do not generally start from one.
    # (e.g. Talmud Bavli pages start from 2)
    def default_starting_page(self) -> int:
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
        unit = units[interval.iteration-1]
        return Unit(unit) if isinstance(unit, str) else Unit(*unit)

    def skip_unit(self) -> Optional[Unit]:
        return None

    def is_skip_interval(self, interval: Interval) -> bool:
        return False

    def tiered_units_for_interval(self, units: Union[dict, list], interval: Interval) -> Optional[Unit]:
        iteration = interval.iteration
        offset = ((iteration - 1) * self.unit_step()) + 1
        if self.unit_step() > 1:
            offset2 = (offset - 1) + self.unit_step()
        else:
            offset2 = None
        offsets = list(filter(None.__ne__, [offset, offset2]))
        targets = list(map(lambda o: [o, []], offsets))
        results = self.find_offset_units(units, targets)
        if set(map(lambda r: r[0], results)) != {0}:
            return None
        paths = list(map(lambda r: r[1], results))
        return Unit(*paths)

    def find_offset_units(self, units: dict, targets: list) -> list:
        def unit_reducer(t: list, name: str):
            attributes = units[name]
            if isinstance(attributes, int):
                start = self.starting_page(units, name)
                length = (attributes - start) + 1

                def elem_reducer(o: int, p: list) -> list:
                    if o <= length:
                        return [0, p + [name, (start + 0) - 1]]
                    return [o - length, p]

                head = [e for e in t if e[0] == 0]
                tail = list(map(elem_reducer, [e for e in t if e[0] != 0]))
                return head + tail
            else:
                def named_elem_reducer(o: int, p: list) -> list:
                    return [o, p + [name]]

                def offset_units_reducer(o: int, p: list) -> list:
                    return [o, p] if o == 0 else [o, p[:-1]]

                head = [e for e in t if e[0] == 0]
                offset_units = self.find_offset_units(attributes, list(map(named_elem_reducer, [e for e in t if e[0] != 0])))
                tail = list(map(offset_units_reducer, offset_units))
                return head + tail

        return list(reduce(unit_reducer, units, targets))

    def find_cycle(self, date: JewishDate):
        if self.initial_cycle_date() is not None:
            return Cycle.from_cycle_initiation(self.initial_cycle_date(), self.cycle_end_calculation, date)
        elif self.perpetual_cycle_anchor() is not None:
            return Cycle.from_perpetual_anchor(self.perpetual_cycle_anchor(), self.cycle_end_calculation, date)
        else:
            raise NotImplementedError

    def _jewish_date(self, date):
        return date if isinstance(date, JewishDate) else JewishDate(date)
