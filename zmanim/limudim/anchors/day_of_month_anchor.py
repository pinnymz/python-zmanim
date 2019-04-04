from typing import Optional

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.anchor import Anchor


class DayOfMonthAnchor(Anchor):
    def __init__(self, day):
        self.__day = day

    def next_occurrence(self, jewish_date: JewishDate) -> Optional[JewishDate]:
        occurrence = JewishDate(jewish_date.jewish_year, jewish_date.jewish_month, self.__day)
        if occurrence <= jewish_date:
            self._increment_month(occurrence)
        return occurrence

    def previous_occurrence(self, jewish_date: JewishDate) -> Optional[JewishDate]:
        occurrence = JewishDate(jewish_date.jewish_year, jewish_date.jewish_month, self.__day)
        if occurrence >= jewish_date:
            self._decrement_month(occurrence)
        return occurrence

    def current_or_previous_occurrence(self, jewish_date: JewishDate) -> Optional[JewishDate]:
        occurrence = JewishDate(jewish_date.jewish_year, jewish_date.jewish_month, self.__day)
        if occurrence > jewish_date:
            self._decrement_month(occurrence)
        return occurrence

    @staticmethod
    def _increment_month(jewish_date: JewishDate):
        if jewish_date.jewish_month == jewish_date.months_in_jewish_year():
            jewish_date.jewish_month = 1
        elif jewish_date.jewish_month == 6:
            jewish_date.forward(29)
        else:
            jewish_date.jewish_month += 1

    @staticmethod
    def _decrement_month(jewish_date):
        if jewish_date.jewish_month == 1:
            jewish_date.jewish_month = jewish_date.months_in_jewish_year()
        elif jewish_date.jewish_month == 7:
            back_days = 30 if jewish_date.jewish_day == 30 else 29
            jewish_date.back(back_days)
        else:
            jewish_date.jewish_month -= 1
