"""String manipulation module for formatting the Hebrew dates"""

import logging

from .jewish_date import JewishDate


_LOGGER = logging.getLogger(__name__)


class HebrewDateFormatter:

    TRANSLITERATED_MONTHS = [
        "Nissan", "Iyar", "Sivan", "Tammuz", "Av", "Elul", "Tishrei",
        "Marcheshvan", "Kislev", "Teves", "Shevat", "Adar", "Adar II",
        "Adar I"]

    HEBREW_MONTHS = [
        u"ניסן", u"אייר", u"סיון", u"תמוז", "אב", u"אלול", u"תשרי", u"מרחשון",
        u"כסלו", u"טבת", u"שבט", u"אדר", u"אדר ב", u"אדר א"]

    GERESH = '\''

    GERSHAYIM = '"'

    def __init__(self, *args, **kwargs):
        self.hebrew_format = True
        self.use_long_hebrew_years = True
        self.use_geresh_gershayim = True

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
        """
        Returns a Hebrew formatted string of a number.

        The method can calculate from 0 - 9999.

        * Single digit numbers such as 3, 30 and 100 will be returned with a
          '(Geresh) += as at the end. For example ג', ל' and ק'.
        * Multi digit numbers such as 21 and 769 will be returned with a
          " (Gershayim) between the second to last and last letters.
          For example כ"א, תשכ"ט
        * 15 and 16 will be returned as ט"ו and ט"ז
        * Single digit numbers (years assumed) such as 6000 (%1000=0) will be
          returned as ו' אלפים
        * 0 will return אפס
        """
        if number < 0:
            raise ValueError("negative numbers can't be formatted")
        elif number > 9999:
            raise ValueError("numbers > 9999 can't be formatted")

        ALAFIM = u"אלפים"
        EFES = u"אפס"
        HUNDREDS = ["", u"ק", u"ר", u"ש", u"ת", u"תק", u"תר", u"תש", u"תת",
                    u"תתק"]
        TENS = ["", u"י", u"כ", u"ל", u"מ", u"נ", u"ס", u"ע", u"פ", u"צ"]
        TEN_ENDS = ["", u"י", u"ך", u"ל", u"ם", u"ן", u"ס", u"ע", u"ף", u"ץ"]
        TAV_TAZ = [u"טו", u"טז"]
        ONES = ["", u"א", u"ב", u"ג", u"ד", u"ה", u"ו", u"ז", u"ח", u"ט"]

        if number == 0:  # do we really need this?
            return EFES

        short_number = number % 1000  # discard thousands

        # next check for all possible single Hebrew digit years
        single_digit_number = (
            short_number < 11 or
            (short_number < 100 and short_number % 10 == 0) or
            (short_number <= 400 and short_number % 100 == 0))

        thousands = number // 1000  # get thousands

        string_number = ""

        # append thousands to String
        if number % 1000 == 0:  # in year is 5000, 4000 etc
            string_number += ONES[thousands]
            if self.use_geresh_gershayim:
                string_number += self.GERESH

            string_number += " "
            string_number += ALAFIM  # add # of thousands + word thousand
            return string_number

        elif self.use_long_hebrew_years and number >= 1000:
            # if alafim boolean display thousands
            string_number += ONES[thousands]
            if self.use_geresh_gershayim:
                string_number += self.GERESH  # append thousands quote
            string_number += " "

        number = number % 1000  # remove 1000s
        hundreds = number // 100  # # of hundreds

        string_number += HUNDREDS[hundreds]  # add hundreds to String
        number = number % 100  # remove 100s

        if number == 15:  # special case 15
            string_number += TAV_TAZ[0]
        elif number == 16:  # special case 16
            string_number += TAV_TAZ[1]
        else:
            tens = number // 10
            if number % 10 == 0:  # if evenly divisible by 10
                if not single_digit_number:
                    # end letters so years like 5750 will end with an end nun
                    string_number += TEN_ENDS[tens]
                else:
                    # standard letters so years like 5050 will end with a
                    # regular nun
                    string_number += TENS[tens]
            else:
                string_number += TENS[tens]
                number = number % 10
                string_number += ONES[number]

        if self.use_geresh_gershayim:
            if single_digit_number:
                string_number += self.GERESH  # append single quote
            else:  # append double quote before last digit
                string_number = string_number[:-1] + self.GERSHAYIM + \
                    string_number[-1:]
        return string_number

    def format_month(self, jewish_date: JewishDate) -> str:
        """
        Returns a string of the current Hebrew month

        If the formatter is set to Hebrew, it will return values such as
        "אדר ב'" or "ניסן", otherwise it will return "Adar II" or "Nissan".
        """
        month = jewish_date.jewish_month

        _LOGGER.debug("Formatting month %s", JewishDate.MONTHS(month))

        if self.hebrew_format:
            if (jewish_date.is_jewish_leap_year() and
                    JewishDate.MONTHS(month) == JewishDate.MONTHS.adar):
                # return Adar I, not Adar in a leap year
                return (f"{self.HEBREW_MONTHS[13]}"
                        f"{self.GERESH if self.use_geresh_gershayim else ''}")
            elif (jewish_date.is_jewish_leap_year() and
                    JewishDate.MONTHS(month) == JewishDate.MONTHS.adar_ii):
                return (f"{self.HEBREW_MONTHS[12]}"
                        f"{self.GERESH if self.use_geresh_gershayim else ''}")
            else:
                return self.HEBREW_MONTHS[month - 1]

        else:
            if (jewish_date.is_jewish_leap_year() and
                    JewishDate.MONTHS(month) == JewishDate.MONTHS.adar):
                # return Adar I, not Adar in a leap year
                return self.TRANSLITERATED_MONTHS[13]
            else:
                return self.TRANSLITERATED_MONTHS[month - 1]
