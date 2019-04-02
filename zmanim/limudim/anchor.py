from typing import Optional

from zmanim.hebrew_calendar.jewish_date import JewishDate


class Anchor:
    def next_occurrence(self, jewish_date: JewishDate) -> Optional[JewishDate]:
        raise NotImplementedError

    def previous_occurrence(self, jewish_date: JewishDate) -> Optional[JewishDate]:
        raise NotImplementedError

    def current_or_previous_occurrence(self, jewish_date: JewishDate) -> Optional[JewishDate]:
        raise NotImplementedError
