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

    def omer_tests(self):
        return (
            (dt(2019, 4, 29), u"ט' בעומר", "Omer 9"),
            (dt(2019, 4, 1), u"", ""),
            (dt(2019, 5, 23), u"ל\"ג בעומר", "Lag BaOmer"),
        )

    def number_tests(self):
        return (
            (0, u"אפס", u"אפס"),
            (1, u"א'", u"א"),
            (15, u"ט\"ו", u"טו"),
            (16, u"ט\"ז", u"טז"),
            (20, u"כ'", u"כ"),
            (120, u"ק\"ך", u"קך"),
            (1000, u"א' אלפים", u"א אלפים"),
            (5780, u"ה' תש\"ף", u"ה תשף")
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

    def testFormatNumber(self):
        """Test numbers formatting with geresh"""
        formatter = HebrewDateFormatter()
        for case in self.number_tests():
            actual = formatter.format_hebrew_number(case[0])
            self.assertEqual(actual, case[1])

    def testFormatNumberNoGereshGershayim(self):
        """Test numbers formatting without geresh"""
        formatter = HebrewDateFormatter(use_geresh_gershayim=False)
        for case in self.number_tests():
            actual = formatter.format_hebrew_number(case[0])
            self.assertEqual(actual, case[2])

    def testFormatNumberOutOfBounds(self):
        """Check for out of bounds number formatting"""
        formatter = HebrewDateFormatter()
        for number in [-1, 10000, 99999]:
            self.assertRaises(
                ValueError, formatter.format_hebrew_number, number)

    def testFormatOmerHebrew(self):
        """Test Omer count in Hebrew"""
        formatter = HebrewDateFormatter(hebrew_format=True)
        for case in self.omer_tests():
            actual = formatter.format_omer(JewishCalendar(case[0]))
            self.assertEqual(actual, case[1])

    def testFormatOmerEnglish(self):
        """Test Omer count in English"""
        formatter = HebrewDateFormatter(hebrew_format=False)
        for case in self.omer_tests():
            actual = formatter.format_omer(JewishCalendar(case[0]))
            self.assertEqual(actual, case[2])
