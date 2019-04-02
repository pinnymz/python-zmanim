from typing import Optional

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.anchor import Anchor


class DayOfYearAnchor(Anchor):
    def __init__(self, month, day):
        self.__month = month
        self.__day = day

    def next_occurrence(self, jewish_date: JewishDate) -> Optional[JewishDate]:
        occurrence = JewishDate(jewish_date.jewish_year, self.__month, self.__day)
        if occurrence <= jewish_date:
            occurrence.jewish_year += 1
        return occurrence

    def previous_occurrence(self, jewish_date: JewishDate) -> Optional[JewishDate]:
        occurrence = JewishDate(jewish_date.jewish_year, self.__month, self.__day)
        if occurrence >= jewish_date:
            occurrence.jewish_year -= 1
        return occurrence

    def current_or_previous_occurrence(self, jewish_date: JewishDate) -> Optional[JewishDate]:
        occurrence = JewishDate(jewish_date.jewish_year, self.__month, self.__day)
        if occurrence > jewish_date:
            occurrence.jewish_year -= 1
        return occurrence
