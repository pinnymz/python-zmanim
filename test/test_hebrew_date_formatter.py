"""Test formatting of the hebrew date"""

import unittest
from datetime import datetime as dt

from zmanim.hebrew_calendar.hebrew_date_formatter import HebrewDateFormatter
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar


class TestHebrewDateFormatter(unittest.TestCase):
    def formatting_tests(self):
        return (
            (dt(2019, 4, 8), u"ג' ניסן ה' תשע\"ט", "3 Nissan, 5779"),
            (dt(2019, 4, 1), u"כ\"ה אדר ב' ה' תשע\"ט", "25 Adar II, 5779"),
            (dt(2019, 3, 1), u"כ\"ד אדר א' ה' תשע\"ט", "24 Adar I, 5779"),
        )

    def testFormatHebrew(self):
        """Test JewishDate with formatter set to Hebrew"""
        formatter = HebrewDateFormatter(hebrew_format=True)
        for case in self.formatting_tests():
            actual = formatter.format(JewishCalendar(case[0]))
            self.assertEqual(actual, case[1])

    def testFormatEnglish(self):
        """Test JewishDate with formatter set to English"""
        formatter = HebrewDateFormatter(hebrew_format=False)
        for case in self.formatting_tests():
            actual = formatter.format(JewishCalendar(case[0]))
            self.assertEqual(actual, case[2])
