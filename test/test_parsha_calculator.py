import unittest

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.calculators.parsha import Parsha


class TestParshaCalculator(unittest.TestCase):
    def test_simple_date(self):
        date = JewishDate(5778, 10, 8)
        limud = Parsha().limud(date)
        self.assertEqual(limud.end_date().jewish_date, (5778, 10, 12))
        self.assertEqual(limud.description(), 'vayechi')

    def test_wraparound_date(self):
        date = JewishDate(5777, 6, 27)
        limud = Parsha().limud(date)
        self.assertEqual(limud.end_date().jewish_date, (5778, 7, 3))
        self.assertEqual(limud.description(), 'haazinu')

    def test_date_before_cycle_restarts(self):
        date = JewishDate(5778, 7, 4)
        limud = Parsha().limud(date)
        self.assertEqual(limud.end_date().jewish_date, (5778, 7, 23))
        self.assertEqual(limud.description(), 'vezos_haberacha')

    def test_disparate_parsha_in_israel(self):
        date = JewishDate(5775, 1, 27)
        limud = Parsha(in_israel=True).limud(date)
        self.assertEqual(limud.end_date().jewish_date, (5775, 1, 29))
        self.assertEqual(limud.description(), 'tazria - metzora')

    def test_disparate_parsha_outside_israel(self):
        date = JewishDate(5775, 1, 27)
        limud = Parsha().limud(date)
        self.assertEqual(limud.end_date().jewish_date, (5775, 1, 29))
        self.assertEqual(limud.description(), 'shemini')
