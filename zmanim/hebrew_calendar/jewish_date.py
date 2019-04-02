import copy
from datetime import date, timedelta
from enum import Enum
from typing import Optional


class JewishDate:
    MONTHS = Enum('Months', 'nissan iyar sivan tammuz av elul tishrei cheshvan kislev teves shevat adar adar_ii')

    RD = date(1, 1, 1)
    JEWISH_EPOCH = -1373429

    CHALAKIM_PER_MINUTE = 18
    CHALAKIM_PER_HOUR = CHALAKIM_PER_MINUTE * 60
    CHALAKIM_PER_DAY = CHALAKIM_PER_HOUR * 24
    CHALAKIM_PER_MONTH = int(CHALAKIM_PER_DAY * 29.5) + 793

    CHALAKIM_MOLAD_TOHU = CHALAKIM_PER_DAY + (CHALAKIM_PER_HOUR * 5) + 204

    CHESHVAN_KISLEV_KEVIAH = Enum('Kviah', 'chaseirim kesidran shelaimim')

    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            self.reset_date()
        elif len(args) == 3:
            self.set_jewish_date(*args, **kwargs)
        elif len(args) == 1 and isinstance(args[0], date):
            self.date = args[0]
        elif len(args) == 1 and isinstance(args[0], int):
            self._set_from_molad(*args)
        else:
            raise ValueError("invalid arguments for new JewishDate")

    def __repr__(self):
        return "<%s gregorian_date=%r, jewish_date=%r, day_of_week=%r, molad_hours=%r, molad_minutes=%r, molad_chalakim=%r>" % \
               (self.__module__ + "." + self.__class__.__qualname__, self.gregorian_date,
                self.jewish_date, self.day_of_week, self.molad_hours, self.molad_minutes, self.molad_chalakim)

    @property
    def gregorian_date(self) -> date:
        return self.__gregorian_date

    @property
    def gregorian_year(self) -> int:
        return self.gregorian_date.year

    @gregorian_year.setter
    def gregorian_year(self, year: int):
        self.set_gregorian_date(year, self.gregorian_month, self.gregorian_day)

    @property
    def gregorian_month(self) -> int:
        return self.gregorian_date.month

    @gregorian_month.setter
    def gregorian_month(self, month: int):
        self.set_gregorian_date(self.gregorian_year, month, self.gregorian_day)

    @property
    def gregorian_day(self) -> int:
        return self.gregorian_date.day

    @gregorian_day.setter
    def gregorian_day(self, day: int):
        self.set_gregorian_date(self.gregorian_year, self.gregorian_month, day)

    @property
    def day_of_week(self) -> int:
        return self.__day_of_week

    @property
    def jewish_date(self) -> (int, int, int):
        return self.__jewish_year, self.__jewish_month, self.__jewish_day

    @property
    def jewish_year(self) -> int:
        return self.__jewish_year

    @jewish_year.setter
    def jewish_year(self, year: int):
        self.set_jewish_date(year, self.jewish_month, self.jewish_day)

    @property
    def jewish_month(self) -> int:
        return self.__jewish_month

    @jewish_month.setter
    def jewish_month(self, month: int):
        self.set_jewish_date(self.jewish_year, month, self.jewish_day)

    @property
    def jewish_day(self) -> int:
        return self.__jewish_day

    @jewish_day.setter
    def jewish_day(self, day: int):
        self.set_jewish_date(self.jewish_year, self.jewish_month, day)

    @property
    def molad_hours(self) -> int:
        return self.__molad_hours

    @property
    def molad_minutes(self) -> int:
        return self.__molad_minutes

    @property
    def molad_chalakim(self) -> int:
        return self.__molad_chalakim

    def __date(self, gregorian_date):
        self.__gregorian_date = gregorian_date
        self.__absolute_date = self._gregorian_date_to_abs_date(gregorian_date)
        self._reset_day_of_week()
        self.__molad_hours = self.__molad_minutes = self.__molad_chalakim = 0
        jewish_year, jewish_month, jewish_day = self._jewish_date_from_abs_date(self.__absolute_date)
        self.__jewish_year = jewish_year
        self.__jewish_month = jewish_month
        self.__jewish_day = jewish_day

    date = property(fset=__date)

    @classmethod
    def from_molad(cls, molad: int) -> 'JewishDate':
        return cls(molad)

    @classmethod
    def from_jewish_date(cls, year: int, month: int, date: int) -> 'JewishDate':
        return cls(year, month, date)

    @classmethod
    def from_date(cls, date: date) -> 'JewishDate':
        return cls(date)

    def reset_date(self) -> 'JewishDate':
        self.date = date.today()
        return self

    def set_jewish_date(self, year: int, month: int, day: int, hours: int = 0, minutes: int = 0, chalakim: int = 0):
        if year < 1 or month < 1 or month > 13 or day < 1 or day > 30 \
                or hours < 0 or hours > 23 or minutes < 0 or minutes > 59 or chalakim < 0 or chalakim > 17:
            raise ValueError("invalid date parts")
        max_months = self.months_in_jewish_year(year)
        month = max_months if month > max_months else month
        max_days = self.days_in_jewish_month(month, year)
        day = max_days if day > max_days else day
        abs_date = self._jewish_date_to_abs_date(year, month, day)
        if abs_date < 0:
            raise ValueError("unsupported early date")
        self.date = self._gregorian_date_from_abs_date(abs_date)
        self.__molad_hours = hours
        self.__molad_minutes = minutes
        self.__molad_chalakim = chalakim

    def set_gregorian_date(self, year: int, month: int, day: int):
        if year < 1 or month < 1 or month > 12 or day < 1 or day > 31:
            raise ValueError("invalid date parts")
        max_days = self.days_in_gregorian_month(month, year)
        day = max_days if day > max_days else day
        self.date = date(year, month, day)

    def forward(self, increment: int = 1) -> 'JewishDate':
        if increment < 0:
            return self.back(-increment)
        if increment > 500:
            self.date = self.gregorian_date + timedelta(days=increment)
            return self
        days_of_year = self.sorted_days_in_jewish_year()
        y, m, d = self.jewish_year, self.jewish_month, self.jewish_day
        d += increment

        def find_days_in_month(month, doy) -> int:
            return next(pair[1] for pair in doy if pair[0] == month)

        days_in_month = find_days_in_month(m, days_of_year)
        while d > days_in_month:
            d -= days_in_month
            m += 1
            if m > len(days_of_year):
                m = 1
            if m == 7:
                y += 1
                days_of_year = self.sorted_days_in_jewish_year(y)
            days_in_month = find_days_in_month(m, days_of_year)

        self.__gregorian_date += timedelta(days=increment)
        self.__absolute_date += increment
        self._reset_day_of_week()
        self.__jewish_year = y
        self.__jewish_month = m
        self.__jewish_day = d
        return self

    def back(self, decrement: int = 1) -> 'JewishDate':
        if decrement < 0:
            return self.forward(-decrement)
        if decrement > 500:
            self.date = self.gregorian_date - timedelta(days=decrement)
            return self
        days_of_year = self.sorted_days_in_jewish_year()
        y, m, d = self.jewish_year, self.jewish_month, self.jewish_day
        d -= decrement

        def find_days_in_month(month, doy) -> int:
            return next(pair[1] for pair in doy if pair[0] == month)

        while d <= 0:
            m -= 1
            if m == 0:
                m = days_of_year.length
            if m == 6:
                y -= 1
                days_of_year = self.sorted_days_in_jewish_year(y)
            d += find_days_in_month(m, days_of_year)

        self.__gregorian_date -= timedelta(days=decrement)
        self.__absolute_date -= decrement
        self._reset_day_of_week()
        self.__jewish_year = y
        self.__jewish_month = m
        self.__jewish_day = d
        return self

    def __add__(self, addend) -> 'JewishDate':
        if isinstance(addend, int):
            return copy.copy(self).forward(addend)
        elif isinstance(addend, timedelta):
            return JewishDate(self.gregorian_date + addend)
        raise ValueError

    def __sub__(self, subtrahend):
        if isinstance(subtrahend, int):
            return copy.copy(self).back(subtrahend)
        elif isinstance(subtrahend, timedelta):
            return JewishDate(self.gregorian_date - subtrahend)
        elif isinstance(subtrahend, JewishDate):
            return self.gregorian_date - subtrahend.gregorian_date
        elif isinstance(subtrahend, date):
            return self.gregorian_date - subtrahend
        raise ValueError

    def __eq__(self, other):
        if isinstance(other, JewishDate):
            return self.gregorian_date == other.gregorian_date
        else:
            return self.gregorian_date == other

    def __ne__(self, other):
        if isinstance(other, JewishDate):
            return self.gregorian_date != other.gregorian_date
        else:
            return self.gregorian_date != other

    def __lt__(self, other):
        if isinstance(other, JewishDate):
            return self.gregorian_date < other.gregorian_date
        else:
            return self.gregorian_date < other

    def __le__(self, other):
        if isinstance(other, JewishDate):
            return self.gregorian_date <= other.gregorian_date
        else:
            return self.gregorian_date <= other

    def __gt__(self, other):
        if isinstance(other, JewishDate):
            return self.gregorian_date > other.gregorian_date
        else:
            return self.gregorian_date > other

    def __ge__(self, other):
        if isinstance(other, JewishDate):
            return self.gregorian_date >= other.gregorian_date
        else:
            return self.gregorian_date >= other

    def days_in_gregorian_year(self, year: Optional[int] = None) -> int:
        if year is None:
            year = self.gregorian_year
        return 366 if self.is_gregorian_leap_year(year) else 365

    def days_in_gregorian_month(self, month: Optional[int] = None, year: Optional[int] = None) -> int:
        if month is None:
            month = self.gregorian_month
        if year is None:
            year = self.gregorian_year
        if month == 2:
            return 29 if self.is_gregorian_leap_year(year) else 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31

    def is_gregorian_leap_year(self, year: Optional[int] = None) -> bool:
        if year is None:
            year = self.gregorian_year
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def months_in_jewish_year(self, year: Optional[int] = None) -> int:
        if year is None:
            year = self.jewish_year
        return 13 if self.is_jewish_leap_year(year) else 12

    # Returns the list of jewish months for a given jewish year in chronological order
    #   sorted_months_in_jewish_year(5779)
    #   => [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6]
    def sorted_months_in_jewish_year(self, year: Optional[int] = None) -> list:
        if year is None:
            year = self.jewish_year
        return sorted(range(1, self.months_in_jewish_year(year) + 1), key=lambda y: (0 if y >= 7 else 1, y))

    # Returns the number of days in each jewish month for a given jewish year in chronological order
    #   sorted_days_in_jewish_year(5779)
    #   => [(7, 30), (8, 29), (9, 30), (10, 29), (11, 30), (12, 30), (13, 29), (1, 30), (2, 29), (3, 30), (4, 29), (5, 30), (6, 29)]
    def sorted_days_in_jewish_year(self, year: Optional[int] = None) -> list:
        if year is None:
            year = self.jewish_year
        return list(map(lambda month: (month, self.days_in_jewish_month(month, year)), self.sorted_months_in_jewish_year(year)))

    def days_in_jewish_year(self, year: Optional[int] = None) -> int:
        if year is None:
            year = self.jewish_year
        return self._jewish_calendar_elapsed_days(year + 1) - self._jewish_calendar_elapsed_days(year)

    def days_in_jewish_month(self, month: Optional[int] = None, year: Optional[int] = None) -> int:
        if month is None:
            month = self.jewish_month
        if year is None:
            year = self.jewish_year
        if month < 1 or month > self.months_in_jewish_year(year):
            raise ValueError("invalid month number")
        m = self.jewish_month_name(month)
        if (m in ('iyar', 'tammuz', 'elul', 'teves', 'adar_ii')) or \
                (m == 'cheshvan' and self.is_cheshvan_short(year)) or \
                (m == 'kislev' and self.is_kislev_short(year)) or \
                (m == 'adar' and not self.is_jewish_leap_year(year)):
            return 29
        return 30

    def day_number_of_jewish_year(self, year: Optional[int] = None, month: Optional[int] = None, day: Optional[int] = None) -> int:
        if year is None:
            year = self.jewish_year
        if month is None:
            month = self.jewish_month
        if day is None:
            day = self.jewish_day
        month_index = self._month_number_from_tishrei(year, month) - 1
        prior_months = self.sorted_months_in_jewish_year(year)[:month_index]
        return day + sum(self.days_in_jewish_month(m, year) for m in prior_months)

    def is_cheshvan_long(self, year: Optional[int] = None) -> bool:
        if year is None:
            year = self.jewish_year
        return self.days_in_jewish_year(year) % 10 == 5

    def is_cheshvan_short(self, year: Optional[int] = None) -> bool:
        return not self.is_cheshvan_long(year)

    def is_kislev_long(self, year: Optional[int] = None) -> bool:
        return not self.is_kislev_short(year)

    def is_kislev_short(self, year: Optional[int] = None) -> bool:
        if year is None:
            year = self.jewish_year
        return self.days_in_jewish_year(year) % 10 == 3

    def is_jewish_leap_year(self, year: Optional[int] = None) -> bool:
        if year is None:
            year = self.jewish_year
        return ((7 * year) + 1) % 19 < 7

    def cheshvan_kislev_kviah(self, year: Optional[int] = None) -> str:
        if year is None:
            year = self.jewish_year
        year_type = (self.days_in_jewish_year(year) % 10) - 3
        return list(self.CHESHVAN_KISLEV_KEVIAH)[year_type]

    def kviah(self, year: Optional[int] = None) -> tuple:
        if year is None:
            year = self.jewish_year
        date = JewishDate(year, 7, 1)
        kviah_value = date.cheshvan_kislev_kviah()
        rosh_hashana_day = date.day_of_week
        date.jewish_month = 1
        pesach_day = date.day_of_week
        return rosh_hashana_day, kviah_value, pesach_day

    def molad(self, month: int = None, year: Optional[int] = None) -> 'JewishDate':
        if month is None:
            month = self.jewish_month
        if year is None:
            year = self.jewish_year
        return self.from_molad(self._chalakim_since_molad_tohu(year, month))

    def jewish_month_name(self, month: Optional[int] = None) -> str:
        if month is None:
            month = self.jewish_month
        return list(self.MONTHS)[month - 1].name

    def jewish_month_from_name(self, month_name: str) -> int:
        return next(m.value for m in self.MONTHS if m.name == month_name)

    def _set_from_molad(self, molad: int):
        gregorian_date = self._gregorian_date_from_abs_date(self._molad_to_abs_date(molad))
        remainder = molad % self.CHALAKIM_PER_DAY
        molad_hours, remainder = divmod(remainder, self.CHALAKIM_PER_HOUR)
        # molad hours start at 18:00, which means that
        # we cross a secular date boundary if hours are 6 or greater
        if molad_hours >= 6:
            gregorian_date += timedelta(days=1)
        self.date = gregorian_date
        # Normalize hours to start at 00:00
        self.__molad_hours = (molad_hours + 18) % 24
        minutes, chalakim = divmod(remainder, self.CHALAKIM_PER_MINUTE)
        self.__molad_minutes = minutes
        self.__molad_chalakim = chalakim

    def _chalakim_since_molad_tohu(self, year: Optional[int] = None, month: Optional[int] = None) -> int:
        if year is None:
            year = self.jewish_year
        if month is None:
            month = self.jewish_month
        prev_year = year - 1
        months = self._month_number_from_tishrei(year, month) - 1
        cycles, remainder = divmod(prev_year, 19)
        months += int(235 * cycles) + \
            int(12 * remainder) + \
            int(((7 * remainder) + 1) / 19)

        return self.CHALAKIM_MOLAD_TOHU + (self.CHALAKIM_PER_MONTH * months)

    def _month_number_from_tishrei(self, year: int, month: int) -> int:
      leap = self.is_jewish_leap_year(year)
      return 1 + ((month + (6 if leap else 5)) % (13 if leap else 12))

    def _jewish_calendar_elapsed_days(self, year: int) -> int:
        days, remainder = self._molad_components_for_year(year)
        return days + self._dechiyos_count(year, days, remainder)

    def _molad_components_for_year(self, year: int) -> (int, int):
        chalakim = self._chalakim_since_molad_tohu(year, 7)  # chalakim up to tishrei of given year
        days, remainder = divmod(chalakim, self.CHALAKIM_PER_DAY)
        return int(days), int(remainder)

    def _dechiyos_count(self, year: int, days: int, remainder: int) -> int:
        count = 0
        # 'days' is Monday-based due to start of Molad at BaHaRaD
        # add 1 to convert to Sunday-based, '0' represents Shabbos
        rosh_hashana_day = (days + 1) % 7
        if (remainder >= 19440) or \
            ((rosh_hashana_day == 3) and (remainder >= 9924) and not self.is_jewish_leap_year(year)) or \
            ((rosh_hashana_day == 2) and (remainder >= 16789) and self.is_jewish_leap_year(year-1)):
            count = 1
        if ((rosh_hashana_day + count) % 7) in [1, 4, 6]:
            count += 1
        return count

    def _jewish_year_start_to_abs_date(self, year: int) -> int:
        return self._jewish_calendar_elapsed_days(year) + self.JEWISH_EPOCH + 1

    def _jewish_date_to_abs_date(self, year: int, month: int, day: int) -> int:
        return self.day_number_of_jewish_year(year, month, day) + \
               self._jewish_year_start_to_abs_date(year) - 1

    def _jewish_date_from_abs_date(self, absolute_date: int) -> (int, int, int):
        jewish_year = int((absolute_date - self.JEWISH_EPOCH) / 366)

        # estimate may be low for CE
        while absolute_date >= self._jewish_year_start_to_abs_date(jewish_year + 1):
            jewish_year += 1

        # estimate may be high for BCE
        while absolute_date < self._jewish_year_start_to_abs_date(jewish_year):
            jewish_year -= 1

        months = self.sorted_months_in_jewish_year(jewish_year)
        jewish_month = next((m for i, m in enumerate(months[:len(months)-1]) if absolute_date < self._jewish_date_to_abs_date(jewish_year, months[i + 1], 1)), months[len(months) - 1])

        jewish_day = absolute_date - self._jewish_date_to_abs_date(jewish_year, jewish_month, 1) + 1

        return jewish_year, jewish_month, jewish_day

    def _gregorian_date_to_abs_date(self, gregorian_date: date) -> int:
        return gregorian_date.toordinal()

    def _gregorian_date_from_abs_date(self, absolute_date: int) -> date:
        return date.fromordinal(absolute_date)

    def _molad_to_abs_date(self, chalakim: int) -> int:
        return int(chalakim / self.CHALAKIM_PER_DAY) + self.JEWISH_EPOCH

    def _reset_day_of_week(self):
        self.__day_of_week = (self.gregorian_date.isoweekday() % 7) + 1
