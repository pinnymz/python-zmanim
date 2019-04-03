import unittest
from datetime import date

from zmanim.limudim.calculators.daf_yomi_bavli import DafYomiBavli


class TestDafYomiBavliCalculator(unittest.TestCase):
    def test_simple_date(self):
        test_date = date(2017, 12, 28)
        limud = DafYomiBavli().limud(test_date)
        self.assertEqual(limud.start_date(), test_date)
        self.assertEqual(limud.end_date(), test_date)
        self.assertEqual(limud.description(), 'shevuos 30')

    def test_before_cycle_began(self):
        test_date = date(1920, 1, 1)
        limud = DafYomiBavli().limud(test_date)
        self.assertIsNone(limud)

    def test_first_day_of_cycle(self):
        test_date = date(2012, 8, 3)
        limud = DafYomiBavli().limud(test_date)
        self.assertEqual(limud.description(), 'berachos 2')

    def test_last_day_of_cycle(self):
        test_date = date(2020, 1, 4)
        limud = DafYomiBavli().limud(test_date)
        self.assertEqual(limud.description(), 'niddah 73')

    def test_before_shekalim_transition_end_of_shekalim(self):
        test_date = date(1969, 4, 28)
        limud = DafYomiBavli().limud(test_date)
        self.assertEqual(limud.description(), 'shekalim 13')

    def test_before_shekalim_transition_beginning_of_yoma(self):
        test_date = date(1969, 4, 29)
        limud = DafYomiBavli().limud(test_date)
        self.assertEqual(limud.description(), 'yoma 2')

    def test_end_of_meilah(self):
        test_date = date(2019, 10, 9)
        limud = DafYomiBavli().limud(test_date)
        self.assertEqual(limud.description(), 'meilah 22')

    def test_beginning_of_kinnim(self):
        test_date = date(2019, 10, 10)
        limud = DafYomiBavli().limud(test_date)
        self.assertEqual(limud.description(), 'kinnim 23')

    def test_beginning_of_tamid(self):
        test_date = date(2019, 10, 13)
        limud = DafYomiBavli().limud(test_date)
        self.assertEqual(limud.description(), 'tamid 26')

    def test_beginning_of_midos(self):
        test_date = date(2019, 10, 22)
        limud = DafYomiBavli().limud(test_date)
        self.assertEqual(limud.description(), 'midos 35')

    def test_after_midos(self):
        test_date = date(2019, 10, 25)
        limud = DafYomiBavli().limud(test_date)
        self.assertEqual(limud.description(), 'niddah 2')
