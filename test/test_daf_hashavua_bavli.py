import unittest
from datetime import date, timedelta

from zmanim.limudim.calculators.daf_hashavua_bavli import DafHashavuaBavli


class TestDafHashavuaBavli(unittest.TestCase):
    def test_simple_date(self):
        test_date = date(2018, 10, 10)
        limud = DafHashavuaBavli().limud(test_date)
        self.assertEqual(limud.start_date(), test_date - timedelta(days=3))
        self.assertEqual(limud.end_date(), test_date + timedelta(days=3))
        self.assertEqual(limud.description(), 'megillah 3')

    def test_before_cycle_began(self):
        test_date = date(2005, 3, 1)
        limud = DafHashavuaBavli().limud(test_date)
        self.assertIsNone(limud)

    def test_first_day_of_cycle(self):
        test_date = date(2057, 2, 11)
        limud = DafHashavuaBavli().limud(test_date)
        self.assertEqual(limud.description(), 'berachos 2')

    def test_last_day_of_cycle(self):
        test_date = date(2057, 2, 10)
        limud = DafHashavuaBavli().limud(test_date)
        self.assertEqual(limud.description(), 'niddah 73')
