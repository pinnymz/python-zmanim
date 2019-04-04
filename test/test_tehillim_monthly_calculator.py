import unittest

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.calculators.tehillim_monthly import TehillimMonthly


class TestTehillimMonthlyCalculator(unittest.TestCase):
    def test_simple_date(self):
        test_date = JewishDate(5778, 10, 8)
        limud = TehillimMonthly().limud(test_date)
        self.assertEqual(limud.start_date(), test_date)
        self.assertEqual(limud.end_date(), test_date)
        self.assertEqual(limud.description(), '44 - 48')

    def test_beginning_of_month(self):
        test_date = JewishDate(5778, 10, 1)
        limud = TehillimMonthly().limud(test_date)
        self.assertEqual(limud.description(), '1 - 9')

    def test_end_of_short_month(self):
        test_date = JewishDate(5778, 10, 29)
        limud = TehillimMonthly().limud(test_date)
        self.assertEqual(limud.description(), '140 - 150')

    def test_end_of_long_month(self):
        test_date = JewishDate(5778, 11, 30)
        limud = TehillimMonthly().limud(test_date)
        self.assertEqual(limud.description(), '145 - 150')

    def test_29th_day_of_long_month(self):
        test_date = JewishDate(5778, 11, 29)
        limud = TehillimMonthly().limud(test_date)
        self.assertEqual(limud.description(), '140 - 144')

    def test_day_25_special_case(self):
        test_date = JewishDate(5778, 11, 25)
        limud = TehillimMonthly().limud(test_date)
        self.assertEqual(limud.description(), '119 1-30')

    def test_day_26_special_case(self):
        test_date = JewishDate(5778, 11, 26)
        limud = TehillimMonthly().limud(test_date)
        self.assertEqual(limud.description(), '119 40-400')
