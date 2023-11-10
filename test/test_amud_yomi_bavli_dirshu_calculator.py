import unittest
from datetime import date

from zmanim.limudim.calculators.amud_yomi_bavli_dirshu import AmudYomiBavliDirshu


class TestAmudYomiBavliDirshuCalculator(unittest.TestCase):
    def test_simple_date(self):
        test_date = date(2024, 5, 30)
        limud = AmudYomiBavliDirshu().limud(test_date)
        self.assertEqual(limud.start_date(), test_date)
        self.assertEqual(limud.end_date(), test_date)
        self.assertEqual(limud.description(), 'shabbos 53a')

    def test_before_cycle_began(self):
        test_date = date(2023, 1, 1)
        limud = AmudYomiBavliDirshu().limud(test_date)
        self.assertIsNone(limud)

    def test_first_day_of_cycle(self):
        test_date = date(2038, 8, 4)
        limud = AmudYomiBavliDirshu().limud(test_date)
        self.assertEqual(limud.start_date(), test_date)
        self.assertEqual(limud.end_date(), test_date)
        self.assertEqual(limud.description(), 'berachos 2a')

    def test_last_day_of_cycle(self):
        test_date = date(2038, 8, 3)
        limud = AmudYomiBavliDirshu().limud(test_date)
        self.assertEqual(limud.description(), 'niddah 73a')

    def test_end_of_meilah(self):
        test_date = date(2038, 2, 10)
        limud = AmudYomiBavliDirshu().limud(test_date)
        self.assertEqual(limud.description(), 'meilah 22a')

    def test_beginning_of_kinnim(self):
        test_date = date(2038, 2, 11)
        limud = AmudYomiBavliDirshu().limud(test_date)
        self.assertEqual(limud.description(), 'kinnim 22b')

    def test_end_of_kinnim(self):
        test_date = date(2038, 2, 16)
        limud = AmudYomiBavliDirshu().limud(test_date)
        self.assertEqual(limud.description(), 'kinnim 25a')

    def test_beginning_of_tamid(self):
        test_date = date(2038, 2, 17)
        limud = AmudYomiBavliDirshu().limud(test_date)
        self.assertEqual(limud.description(), 'tamid 25b')

    def test_end_of_tamid(self):
        test_date = date(2038, 3, 5)
        limud = AmudYomiBavliDirshu().limud(test_date)
        self.assertEqual(limud.description(), 'tamid 33b')

    def test_beginning_of_midos(self):
        test_date = date(2038, 3, 6)
        limud = AmudYomiBavliDirshu().limud(test_date)
        self.assertEqual(limud.description(), 'midos 34a')

    def test_end_of_midos(self):
        test_date = date(2038, 3, 13)
        limud = AmudYomiBavliDirshu().limud(test_date)
        self.assertEqual(limud.description(), 'midos 37b')

    def test_after_midos(self):
        test_date = date(2038, 3, 14)
        limud = AmudYomiBavliDirshu().limud(test_date)
        self.assertEqual(limud.description(), 'niddah 2a')
