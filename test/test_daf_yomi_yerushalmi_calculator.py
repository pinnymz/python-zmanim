import unittest
from datetime import date

from zmanim.limudim.calculators.daf_yomi_yerushalmi import DafYomiYerushalmi
from zmanim.hebrew_calendar.jewish_date import JewishDate


class TestDafYomiYerushalmiCalculator(unittest.TestCase):
    def test_simple_date(self):
        test_date = date(2017, 12, 28)
        limud = DafYomiYerushalmi().limud(test_date)
        self.assertEqual(limud.start_date(), test_date)
        self.assertEqual(limud.end_date(), test_date)
        self.assertEqual(limud.description(), 'bava_metzia 33')

    def test_before_cycle_began(self):
        test_date = date(1980, 1, 1)
        limud = DafYomiYerushalmi().limud(test_date)
        self.assertIsNone(limud)

    def test_first_day_of_cycle(self):
        test_date = date(2005, 10, 3)
        limud = DafYomiYerushalmi().limud(test_date)
        self.assertEqual(limud.description(), 'berachos 1')

    def test_last_day_of_cycle(self):
        test_date = date(2010, 1, 12)
        limud = DafYomiYerushalmi().limud(test_date)
        self.assertEqual(limud.description(), 'niddah 13')

    def test_last_skip_day(self):
        test_date = JewishDate(5778, 7, 10)
        limud = DafYomiYerushalmi().limud(test_date)
        self.assertEqual(limud.start_date(), test_date)
        self.assertEqual(limud.end_date(), test_date)
        self.assertEqual(limud.description(), 'no_daf_today')
