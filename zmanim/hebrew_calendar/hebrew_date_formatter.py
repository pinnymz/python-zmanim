"""String manipulation module for formatting the Hebrew dates"""

from .jewish_date import JewishDate


class HebrewDateFormatter:

    TRANSLITERATED_MONTHS = [
        "Nissan", "Iyar", "Sivan", "Tammuz", "Av", "Elul", "Tishrei",
        "Marcheshvan", "Kislev", "Teves", "Shevat", "Adar", "Adar II",
        "Adar I"]

    HEBREW_MONTHS = [
        u"ניסן", u"אייר", u"סיון", u"תמוז", "אב", u"אלול", u"תשרי", u"מרחשון",
        u"כסלו", u"טבת", u"שבט", u"אדר", u"אדר ב", u"אדר א"]

    def __init__(self, *args, **kwargs):
        self.hebrew_format = True
        if 'hebrew_format' in kwargs:
            self.hebrew_format = kwargs.pop('hebrew_format')

    def format(self, jewish_date: JewishDate) -> str:
        """
        Formats the Jewish date

        If the formatter is set to Hebrew, it will format in the form
        "day Month year" for example כ"א שבט תשכ"ט, and the format
        "21 Shevat, 5729" if not.
        """
        if self.hebrew_format:
            return (f"{self.format_hebrew_number(jewish_date.jewish_day)} "
                    f"{self.format_month(jewish_date)} "
                    f"{self.format_hebrew_number(jewish_date.jewish_year)}")

        return (f"{jewish_date.jewish_day} {self.format_month(jewish_date)}, "
                f"{jewish_date.jewish_year}")

    def format_hebrew_number(self, number: int) -> str:
        pass

    def format_month(self, jewish_date: JewishDate) -> str:
        """
        Returns a string of the current Hebrew month

        If the formatter is set to Hebrew, it will return values such as
        "אדר ב'" or "ניסן", otherwise it will return "Adar II" or "Nissan".
        """
        month = jewish_date.jewish_month
        if self.hebrew_format:
            if (jewish_date.is_jewish_leap_year() and
                    JewishDate.MONTHS(month) == 'adar'):
                # return Adar I, not Adar in a leap year
                return (f"{self.HEBREW_MONTHS[13]}"
                        f"{self.GERESH if self.use_geresh_gershayim else ''}")
            elif (jewish_date.is_jewish_leap_year() and
                    JewishDate.MONTHS(month) == 'adar_ii'):
                return (f"{self.HEBREW_MONTHS[12]}"
                        f"{self.GERESH if self.use_geresh_gershayim else ''}")
            else:
                return self.HEBREW_MONTHS[month - 1]

        else:
            if (jewish_date.is_jewish_leap_year() and
                    JewishDate.MONTHS(month) == 'adar'):
                # return Adar I, not Adar in a leap year
                return self.TRANSLITERATED_MONTHS[13]
            else:
                return self.TRANSLITERATED_MONTHS[month - 1]
