"""Test formatting of the hebrew date"""

import unittest
from datetime import datetime as dt

from zmanim.hebrew_calendar.hebrew_date_formatter import HebrewDateFormatter
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar


class TestHebrewDateFormatter(unittest.TestCase):
    def formatting_tests(self):
        return (
            JewishCalendar(dt(2019, 4, 8)),
            u"ג' ניסן ה' תשע\"ט", "3 Nissan, 5779")

    def testFormatHebrew(self):
        """Test JewishDate with formatter set to Hebrew"""
        formatter = HebrewDateFormatter(hebrew_format=True)
        actual = formatter.format(self.formatting_tests()[0])
        self.assertEqual(actual, self.formatting_tests()[1])

    def testFormatEnglish(self):
        """Test JewishDate with formatter set to Hebrew"""
        formatter = HebrewDateFormatter(hebrew_format=False)
        actual = formatter.format(self.formatting_tests()[0])
        self.assertEqual(actual, self.formatting_tests()[2])
