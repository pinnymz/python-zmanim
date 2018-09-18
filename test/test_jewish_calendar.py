import unittest
from datetime import datetime, timedelta

from dateutil import tz, parser

import test.test_helper
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar


class TestJewishCalendar(unittest.TestCase):
    def all_year_types(self):
        return [test.test_helper.standard_monday_chaseirim(),
                test.test_helper.standard_monday_shelaimim(),
                test.test_helper.standard_tuesday_kesidran(),
                test.test_helper.standard_thursday_kesidran(),
                test.test_helper.standard_thursday_shelaimim(),
                test.test_helper.standard_shabbos_chaseirim(),
                test.test_helper.standard_shabbos_shelaimim(),
                test.test_helper.leap_monday_chaseirim(),
                test.test_helper.leap_monday_shelaimim(),
                test.test_helper.leap_tuesday_kesidran(),
                test.test_helper.leap_thursday_chaseirim(),
                test.test_helper.leap_thursday_shelaimim(),
                test.test_helper.leap_shabbos_chaseirim(),
                test.test_helper.leap_shabbos_shelaimim()]

    def all_rosh_hashanas(self):
        return map(lambda y: JewishCalendar(y, 7, 1), self.all_year_types())

    def chanukah_for_chaseirim(self):
        return ['9-25', '9-26', '9-27', '9-28', '9-29', '10-1', '10-2', '10-3']

    def leap_purim(self):
        return {'purim_katan': ['12-14'],
                'shushan_purim_katan': ['12-15'],
                'taanis_esther': ['13-13'],
                'purim': ['13-14'],
                'shushan_purim': ['13-15']}

    def standard_significant_days(self):
        return {
            'erev_pesach': ['1-14'],
            'pesach': ['1-15', '1-16', '1-21', '1-22'],
            'chol_hamoed_pesach': ['1-17', '1-18', '1-19', '1-20'],
            'pesach_sheni': ['2-14'],
            'erev_shavuos': ['3-5'],
            'shavuos': ['3-6', '3-7'],
            'seventeen_of_tammuz': ['4-17'],
            'tisha_beav': ['5-9'],
            'tu_beav': ['5-15'],
            'erev_rosh_hashana': ['6-29'],
            'rosh_hashana': ['7-1', '7-2'],
            'tzom_gedalyah': ['7-3'],
            'erev_yom_kippur': ['7-9'],
            'yom_kippur': ['7-10'],
            'erev_succos': ['7-14'],
            'succos': ['7-15', '7-16'],
            'chol_hamoed_succos': ['7-17', '7-18', '7-19', '7-20'],
            'hoshana_rabbah': ['7-21'],
            'shemini_atzeres': ['7-22'],
            'simchas_torah': ['7-23'],
            'chanukah': ['9-25', '9-26', '9-27', '9-28', '9-29', '9-30', '10-1', '10-2'],
            'tenth_of_teves': ['10-10'],
            'tu_beshvat': ['11-15'],
            'taanis_esther': ['12-13'],
            'purim': ['12-14'],
            'shushan_purim': ['12-15']
        }

    def leap_significant_days(self):
        return {**self.standard_significant_days(), **self.leap_purim()}

    def israel_standard_significant_days(self):
        significant_days = {
            **self.standard_significant_days(),
            'pesach': ['1-15', '1-21'],
            'chol_hamoed_pesach': ['1-16', '1-17', '1-18', '1-19', '1-20'],
            'shavuos': ['3-6'],
            'succos': ['7-15'],
            'chol_hamoed_succos': ['7-16', '7-17', '7-18', '7-19', '7-20']
        }
        significant_days.pop('simchas_torah')
        return significant_days

    def israel_leap_significant_days(self):
        return {**self.israel_standard_significant_days(), **self.leap_purim()}

    def modern_significant_days(self):
        return ['yom_hashoah', 'yom_hazikaron', 'yom_haatzmaut', 'yom_yerushalayim']

    # test that setup years are all as expected
    def test_all_leap_years_as_expected(self):
        result = map(lambda c: c.is_jewish_leap_year(), self.all_rosh_hashanas())
        self.assertEqual(list(result), [False, False, False, False, False, False, False,
                                        True, True, True, True, True, True, True])

    def test_all_days_of_week_as_expected(self):
        result = map(lambda c: c.day_of_week, self.all_rosh_hashanas())
        self.assertEqual(list(result), [2, 2, 3, 5, 5, 7, 7, 2, 2, 3, 5, 5, 7, 7])

    def test_all_cheshvan_kislev_kviahs_as_expected(self):
        result = map(lambda c: c.cheshvan_kislev_kviah().name, self.all_rosh_hashanas())
        self.assertEqual(list(result), ['chaseirim', 'shelaimim', 'kesidran', 'kesidran',
                                        'shelaimim', 'chaseirim', 'shelaimim', 'chaseirim',
                                        'shelaimim', 'kesidran', 'chaseirim', 'shelaimim',
                                        'chaseirim', 'shelaimim'])

    # real testing starts here
    def test_significant_days_for_standard_monday_chaseirim(self):
        year = test.test_helper.standard_monday_chaseirim()

        result = test.test_helper.all_days_matching(year, lambda c: c.significant_day())
        expected = {**self.standard_significant_days(),
                    'chanukah': self.chanukah_for_chaseirim(),
                    'taanis_esther': ['12-11']}
        self.assertEqual(result, expected)

        israel_result = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), in_israel=True)
        expected = {**self.israel_standard_significant_days(),
                    'chanukah': self.chanukah_for_chaseirim(),
                    'taanis_esther': ['12-11']}
        self.assertEqual(israel_result, expected)

    def test_significant_days_for_standard_monday_shelaimim(self):
        year = test.test_helper.standard_monday_shelaimim()

        result = test.test_helper.all_days_matching(year, lambda c: c.significant_day())
        expected = self.standard_significant_days()
        self.assertEqual(result, expected)

        israel_result = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), in_israel=True)
        expected = self.israel_standard_significant_days()
        self.assertEqual(israel_result, expected)

    def test_significant_days_for_standard_tuesday_kesidran(self):
        year = test.test_helper.standard_tuesday_kesidran()

        result = test.test_helper.all_days_matching(year, lambda c: c.significant_day())
        expected = self.standard_significant_days()
        self.assertEqual(result, expected)

        israel_result = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), in_israel=True)
        expected = self.israel_standard_significant_days()
        self.assertEqual(israel_result, expected)

    def test_significant_days_for_standard_thursday_kesidran(self):
        year = test.test_helper.standard_thursday_kesidran()

        result = test.test_helper.all_days_matching(year, lambda c: c.significant_day())
        expected = {**self.standard_significant_days(),
                    'tzom_gedalyah': ['7-4'],
                    'seventeen_of_tammuz': ['4-18'],
                    'tisha_beav': ['5-10']
                    }
        self.assertEqual(result, expected)

        israel_result = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), in_israel=True)
        expected = {**self.israel_standard_significant_days(),
                    'tzom_gedalyah': ['7-4'],
                    'seventeen_of_tammuz': ['4-18'],
                    'tisha_beav': ['5-10']
                    }
        self.assertEqual(israel_result, expected)

    def test_significant_days_for_standard_thursday_shelaimim(self):
        year = test.test_helper.standard_thursday_shelaimim()

        result = test.test_helper.all_days_matching(year, lambda c: c.significant_day())
        expected = {**self.standard_significant_days(),
                    'tzom_gedalyah': ['7-4']
                    }
        self.assertEqual(result, expected)

        israel_result = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), in_israel=True)
        expected = {**self.israel_standard_significant_days(),
                    'tzom_gedalyah': ['7-4']
                    }
        self.assertEqual(israel_result, expected)

    def test_significant_days_for_standard_shabbos_chaseirim(self):
        year = test.test_helper.standard_shabbos_chaseirim()

        result = test.test_helper.all_days_matching(year, lambda c: c.significant_day())
        expected = {**self.standard_significant_days(),
                    'chanukah': self.chanukah_for_chaseirim()
                    }
        self.assertEqual(result, expected)

        israel_result = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), in_israel=True)
        expected = {**self.israel_standard_significant_days(),
                    'chanukah': self.chanukah_for_chaseirim()
                    }
        self.assertEqual(israel_result, expected)

    def test_significant_days_for_standard_shabbos_shelaimim(self):
        year = test.test_helper.standard_shabbos_shelaimim()

        result = test.test_helper.all_days_matching(year, lambda c: c.significant_day())
        expected = {**self.standard_significant_days(),
                    'taanis_esther': ['12-11']
                    }
        self.assertEqual(result, expected)

        israel_result = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), in_israel=True)
        expected = {**self.israel_standard_significant_days(),
                    'taanis_esther': ['12-11']
                    }
        self.assertEqual(israel_result, expected)

    def test_significant_days_for_leap_monday_chaseirim(self):
        year = test.test_helper.leap_monday_chaseirim()

        result = test.test_helper.all_days_matching(year, lambda c: c.significant_day())
        expected = {**self.leap_significant_days(),
                    'chanukah': self.chanukah_for_chaseirim()
                    }
        self.assertEqual(result, expected)

        israel_result = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), in_israel=True)
        expected = {**self.israel_leap_significant_days(),
                    'chanukah': self.chanukah_for_chaseirim()
                    }
        self.assertEqual(israel_result, expected)

    def test_significant_days_for_leap_monday_shelaimim(self):
        year = test.test_helper.leap_monday_shelaimim()

        result = test.test_helper.all_days_matching(year, lambda c: c.significant_day())
        expected = {**self.leap_significant_days(),
                    'seventeen_of_tammuz': ['4-18'],
                    'tisha_beav': ['5-10']
                    }
        self.assertEqual(result, expected)

        israel_result = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), in_israel=True)
        expected = {**self.israel_leap_significant_days(),
                    'seventeen_of_tammuz': ['4-18'],
                    'tisha_beav': ['5-10']
                    }
        self.assertEqual(israel_result, expected)

    def test_significant_days_for_leap_tuesday_kesidran(self):
        year = test.test_helper.leap_tuesday_kesidran()

        result = test.test_helper.all_days_matching(year, lambda c: c.significant_day())
        expected = {**self.leap_significant_days(),
                    'seventeen_of_tammuz': ['4-18'],
                    'tisha_beav': ['5-10']
                    }
        self.assertEqual(result, expected)

        israel_result = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), in_israel=True)
        expected = {**self.israel_leap_significant_days(),
                    'seventeen_of_tammuz': ['4-18'],
                    'tisha_beav': ['5-10']
                    }
        self.assertEqual(israel_result, expected)

    def test_significant_days_for_leap_thursday_chaseirim(self):
        year = test.test_helper.leap_thursday_chaseirim()

        result = test.test_helper.all_days_matching(year, lambda c: c.significant_day())
        expected = {**self.leap_significant_days(),
                    'tzom_gedalyah': ['7-4'],
                    'chanukah': self.chanukah_for_chaseirim()
                    }
        self.assertEqual(result, expected)

        israel_result = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), in_israel=True)
        expected = {**self.israel_leap_significant_days(),
                    'tzom_gedalyah': ['7-4'],
                    'chanukah': self.chanukah_for_chaseirim()
                    }
        self.assertEqual(israel_result, expected)

    def test_significant_days_for_leap_thursday_shelaimim(self):
        year = test.test_helper.leap_thursday_shelaimim()

        result = test.test_helper.all_days_matching(year, lambda c: c.significant_day())
        expected = {**self.leap_significant_days(),
                    'tzom_gedalyah': ['7-4'],
                    'taanis_esther': ['13-11']
                    }
        self.assertEqual(result, expected)

        israel_result = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), in_israel=True)
        expected = {**self.israel_leap_significant_days(),
                    'tzom_gedalyah': ['7-4'],
                    'taanis_esther': ['13-11']
                    }
        self.assertEqual(israel_result, expected)

    def test_significant_days_for_leap_shabbos_chaseirim(self):
        year = test.test_helper.leap_shabbos_chaseirim()

        result = test.test_helper.all_days_matching(year, lambda c: c.significant_day())
        expected = {**self.leap_significant_days(),
                    'chanukah': self.chanukah_for_chaseirim(),
                    'taanis_esther': ['13-11']
                    }
        self.assertEqual(result, expected)

        israel_result = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), in_israel=True)
        expected = {**self.israel_leap_significant_days(),
                    'chanukah': self.chanukah_for_chaseirim(),
                    'taanis_esther': ['13-11']
                    }
        self.assertEqual(israel_result, expected)

    def test_significant_days_for_leap_shabbos_shelaimim(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        result = test.test_helper.all_days_matching(year, lambda c: c.significant_day())
        expected = self.leap_significant_days()
        self.assertEqual(result, expected)

        israel_result = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), in_israel=True)
        expected = self.israel_leap_significant_days()
        self.assertEqual(israel_result, expected)

    def test_modern_holidays_for_nissan_starting_sunday(self):
        year = test.test_helper.standard_thursday_shelaimim()

        self.assertEqual(JewishCalendar(year, 1, 1).day_of_week, 1)
        all_days = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), use_modern_holidays=True)
        expected = {'yom_hashoah': ['1-26'],
                    'yom_hazikaron': ['2-2'],
                    'yom_haatzmaut': ['2-3'],
                    'yom_yerushalayim': ['2-28']}
        result = test.test_helper.specific_days_matching(all_days, expected.keys())
        self.assertEqual(result, expected)

    def test_modern_holidays_for_nissan_starting_tuesday(self):
        year = test.test_helper.standard_monday_chaseirim()

        self.assertEqual(JewishCalendar(year, 1, 1).day_of_week, 3)
        all_days = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), use_modern_holidays=True)
        expected = {'yom_hashoah': ['1-28'],
                    'yom_hazikaron': ['2-5'],
                    'yom_haatzmaut': ['2-6'],
                    'yom_yerushalayim': ['2-28']}
        result = test.test_helper.specific_days_matching(all_days, expected.keys())
        self.assertEqual(result, expected)

    def test_modern_holidays_for_nissan_starting_thursday(self):
        year = test.test_helper.standard_monday_shelaimim()

        self.assertEqual(JewishCalendar(year, 1, 1).day_of_week, 5)
        all_days = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), use_modern_holidays=True)
        expected = {'yom_hashoah': ['1-27'],
                    'yom_hazikaron': ['2-4'],
                    'yom_haatzmaut': ['2-5'],
                    'yom_yerushalayim': ['2-28']}
        result = test.test_helper.specific_days_matching(all_days, expected.keys())
        self.assertEqual(result, expected)

    def test_modern_holidays_for_nissan_starting_shabbos(self):
        year = test.test_helper.standard_thursday_kesidran()

        self.assertEqual(JewishCalendar(year, 1, 1).day_of_week, 7)
        all_days = test.test_helper.all_days_matching(year, lambda c: c.significant_day(), use_modern_holidays=True)
        expected = {'yom_hashoah': ['1-27'],
                    'yom_hazikaron': ['2-3'],
                    'yom_haatzmaut': ['2-4'],
                    'yom_yerushalayim': ['2-28']}
        result = test.test_helper.specific_days_matching(all_days, expected.keys())
        self.assertEqual(result, expected)

    def test_is_yom_tov_outside_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_yom_tov()).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected = ['7-1', '7-2', '7-10', '7-15', '7-16',
                    '7-17', '7-18', '7-19', '7-20', '7-21', '7-22', '7-23',
                    '9-25', '9-26', '9-27', '9-28', '9-29', '9-30', '10-1', '10-2',
                    '11-15', '12-14', '12-15', '13-14', '13-15',
                    '1-15', '1-16', '1-17', '1-18', '1-19', '1-20', '1-21', '1-22',
                    '2-14', '3-6', '3-7', '5-15']
        self.assertEqual(all_days, expected)

    def test_is_yom_tov_in_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_yom_tov(), in_israel=True).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected = ['7-1', '7-2', '7-10', '7-15', '7-16',
                    '7-17', '7-18', '7-19', '7-20', '7-21', '7-22',
                    '9-25', '9-26', '9-27', '9-28', '9-29', '9-30', '10-1', '10-2',
                    '11-15', '12-14', '12-15', '13-14', '13-15',
                    '1-15', '1-16', '1-17', '1-18', '1-19', '1-20', '1-21',
                    '2-14', '3-6', '5-15']
        self.assertEqual(all_days, expected)

    def test_is_yom_tov_with_modern_holidays(self):
        year = test.test_helper.leap_shabbos_shelaimim()
        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_yom_tov(), use_modern_holidays=True).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        for expected_day in ['1-27', '2-4', '2-5', '2-28']:
            self.assertIn(expected_day, all_days)

    def test_is_yom_tov_assur_bemelacha_outside_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_yom_tov_assur_bemelacha()).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected = ['7-1', '7-2', '7-10', '7-15', '7-16', '7-22', '7-23',
                    '1-15', '1-16', '1-21', '1-22', '3-6', '3-7']
        self.assertEqual(all_days, expected)

    def test_is_yom_tov_assur_bemelacha_in_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_yom_tov_assur_bemelacha(), in_israel=True).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected = ['7-1', '7-2', '7-10', '7-15', '7-22', '1-15', '1-21', '3-6']
        self.assertEqual(all_days, expected)

    def test_is_yom_tov_assur_bemelacha_with_modern_holidays(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_yom_tov_assur_bemelacha(), use_modern_holidays=True).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        for expected_day in ['1-27', '2-4', '2-5', '2-28']:
            self.assertNotIn(expected_day, all_days)  # should not be assur

    def test_is_assur_bemelacha_outside_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_assur_bemelacha()).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected_yom_tov = ['7-1', '7-2', '7-10', '7-15', '7-16', '7-22', '7-23',
                            '1-15', '1-16', '1-21', '1-22', '3-6', '3-7']
        expected_shabbosos = test.test_helper.all_days_matching(year, lambda c: c.day_of_week == 7).values()
        expected_shabbosos = [item for sublist in expected_shabbosos for item in sublist]  # flatten

        self.assertEqual(sorted(all_days), sorted(list(set().union(expected_yom_tov, expected_shabbosos))))

    def test_is_assur_bemelacha_in_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_assur_bemelacha(), in_israel=True).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected_yom_tov = ['7-1', '7-2', '7-10', '7-15', '7-22', '1-15', '1-21', '3-6']
        expected_shabbosos = test.test_helper.all_days_matching(year, lambda c: c.day_of_week == 7).values()
        expected_shabbosos = [item for sublist in expected_shabbosos for item in sublist]  # flatten

        self.assertEqual(sorted(all_days), sorted(list(set().union(expected_yom_tov, expected_shabbosos))))

    def test_is_tomorrow_assur_bemelacha_outside_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_tomorrow_assur_bemelacha()).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected_erev_yom_tov = ['7-9', '7-14', '7-21', '1-14', '1-20', '3-5', '6-29']
        expected_erev_yom_tov_sheni = ['7-1', '7-15', '7-22', '1-15', '1-21', '3-6']

        expected_erev_shabbos = test.test_helper.all_days_matching(year, lambda c: c.day_of_week == 6).values()
        expected_erev_shabbos = [item for sublist in expected_erev_shabbos for item in sublist]  # flatten

        expected = list(set().union(expected_erev_yom_tov, expected_erev_yom_tov_sheni, expected_erev_shabbos))
        self.assertEqual(sorted(all_days), sorted(expected))

    def test_is_tomorrow_assur_bemelacha_in_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_tomorrow_assur_bemelacha(), in_israel=True).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected_erev_yom_tov = ['7-9', '7-14', '7-21', '1-14', '1-20', '3-5', '6-29']
        expected_erev_yom_tov_sheni = ['7-1']

        expected_erev_shabbos = test.test_helper.all_days_matching(year, lambda c: c.day_of_week == 6).values()
        expected_erev_shabbos = [item for sublist in expected_erev_shabbos for item in sublist]  # flatten

        expected = list(set().union(expected_erev_yom_tov, expected_erev_yom_tov_sheni, expected_erev_shabbos))
        self.assertEqual(sorted(all_days), sorted(expected))

    def test_has_delayed_candle_lighting_for_non_candle_lighting_day(self):
        date = '2018-09-13'
        subject = JewishCalendar(parser.parse(date))
        self.assertFalse(subject.has_delayed_candle_lighting())

    def test_has_delayed_candle_lighting_for_standard_erev_shabbos(self):
        date = '2018-09-14'
        subject = JewishCalendar(parser.parse(date))
        self.assertFalse(subject.has_delayed_candle_lighting())

    def test_has_delayed_candle_lighting_for_standard_erev_yom_tov(self):
        date = '2018-09-30'
        subject = JewishCalendar(parser.parse(date))
        self.assertFalse(subject.has_delayed_candle_lighting())

    def test_has_delayed_candle_lighting_for_standard_first_day_yom_tov(self):
        date = '2018-10-01'
        subject = JewishCalendar(parser.parse(date))
        self.assertTrue(subject.has_delayed_candle_lighting())

    def test_has_delayed_candle_lighting_for_yom_tov_erev_shabbos(self):
        date = '2019-04-26'
        subject = JewishCalendar(parser.parse(date))
        self.assertFalse(subject.has_delayed_candle_lighting())

    def test_has_delayed_candle_lighting_for_shabbos_followed_by_yom_tov(self):
        date = '2019-06-08'
        subject = JewishCalendar(parser.parse(date))
        self.assertTrue(subject.has_delayed_candle_lighting())

    def test_is_yom_tov_sheni_outside_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_yom_tov_sheni()).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten

        expected_days = ['7-2', '7-16', '7-23', '1-16', '1-22', '3-7']
        self.assertEqual(all_days, expected_days)

    def test_is_yom_tov_sheni_in_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_yom_tov_sheni(), in_israel=True).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten

        expected_days = ['7-2']
        self.assertEqual(all_days, expected_days)

    def test_is_erev_yom_tov_sheni_outside_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_erev_yom_tov_sheni()).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten

        expected_days = ['7-1', '7-15', '7-22', '1-15', '1-21', '3-6']
        self.assertEqual(all_days, expected_days)

    def test_is_erev_yom_tov_sheni_in_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_erev_yom_tov_sheni(), in_israel=True).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten

        expected_days = ['7-1']
        self.assertEqual(all_days, expected_days)

    def test_is_chol_hamoed_outside_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_chol_hamoed()).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected = ['7-17', '7-18', '7-19', '7-20', '7-21', '1-17', '1-18', '1-19', '1-20']
        self.assertEqual(all_days, expected)

    def test_is_chol_hamoed_in_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_chol_hamoed(), in_israel=True).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected = ['7-16', '7-17', '7-18', '7-19', '7-20', '7-21', '1-16', '1-17', '1-18', '1-19', '1-20']
        self.assertEqual(all_days, expected)

    def test_is_erev_yom_tov_outside_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_erev_yom_tov()).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected = ['7-9', '7-14', '7-21', '1-14', '1-20', '3-5', '6-29']
        self.assertEqual(all_days, expected)

    def test_is_erev_yom_tov_in_israel(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_erev_yom_tov(), in_israel=True).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected = ['7-9', '7-14', '7-21', '1-14', '1-20', '3-5', '6-29']
        self.assertEqual(all_days, expected)

    def test_is_taanis(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_taanis()).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected = ['7-3', '7-10', '10-10', '13-13', '4-17', '5-9']
        self.assertEqual(all_days, expected)

    def test_is_rosh_chodesh(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_rosh_chodesh()).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected = ['7-30', '8-1', '8-30', '9-1', '9-30', '10-1',
                    '11-1', '11-30', '12-1', '12-30', '13-1', '1-1', '1-30',
                    '2-1', '3-1', '3-30', '4-1', '5-1', '5-30', '6-1']
        self.assertEqual(all_days, expected)

    def test_is_erev_rosh_chodesh(self):
        year = test.test_helper.leap_shabbos_shelaimim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_erev_rosh_chodesh()).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected = ['7-29', '8-29', '9-29', '10-29', '11-29', '12-29', '13-29',
                    '1-29', '2-29', '3-29', '4-29', '5-29']
        self.assertEqual(all_days, expected)

    def test_is_chanukah_for_chaseirim_years(self):
        year = test.test_helper.standard_monday_chaseirim()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_chanukah()).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected = self.chanukah_for_chaseirim()
        self.assertEqual(all_days, expected)

    def test_is_chanukah_for_non_chaseirim_years(self):
        year = test.test_helper.standard_tuesday_kesidran()

        all_days = test.test_helper.all_days_matching(year, lambda c: c.is_chanukah()).values()
        all_days = [item for sublist in all_days for item in sublist]  # flatten
        expected = self.standard_significant_days()['chanukah']
        self.assertEqual(all_days, expected)

    def test_day_of_chanukah_for_chaseirim_years(self):
        year = test.test_helper.standard_monday_chaseirim()

        expected_days = map(lambda date: date.split('-'), self.chanukah_for_chaseirim())
        result = map(lambda date: JewishCalendar(year, int(date[0]), int(date[1])).day_of_chanukah(), expected_days)
        self.assertEqual(list(result), list(range(1, 9)))

    def test_day_of_chanukah_for_non_chaseirim_years(self):
        year = test.test_helper.standard_tuesday_kesidran()

        expected_days = map(lambda date: date.split('-'), self.standard_significant_days()['chanukah'])
        result = map(lambda date: JewishCalendar(year, int(date[0]), int(date[1])).day_of_chanukah(), expected_days)
        self.assertEqual(list(result), list(range(1, 9)))

    def test_day_of_chanukah_for_non_chanukah_date(self):
        calendar = JewishCalendar(test.test_helper.standard_monday_chaseirim(), 7, 1)
        self.assertIsNone(calendar.day_of_chanukah())

    def test_day_of_omer(self):
        calendar = JewishCalendar(test.test_helper.standard_monday_chaseirim(), 1, 16)
        found_days = []

        def find_day(c: JewishCalendar):
            found_days.append(c.day_of_omer())
            c.forward()

        for n in range(1, 50):
            find_day(calendar)

        self.assertEqual(found_days, list(range(1, 50)))

    def test_day_of_omer_outside_of_omer(self):
        calendar = JewishCalendar(test.test_helper.standard_monday_chaseirim(), 7, 1)
        self.assertIsNone(calendar.day_of_omer())

    def test_molad_as_datetime(self):
        expected_offset = (2, 20, 56, 496000)  # UTC is 2:20:56.496 behind Jerusalem Local Time
        calendar = JewishCalendar(5776, 8, 1)
        hours, minutes, chalakim = 5, 51, 10
        seconds = (chalakim * 10 / 3.0)
        seconds, microseconds = divmod(seconds * 10**6, 10**6)
        hours -= expected_offset[0]
        minutes -= expected_offset[1]
        seconds -= expected_offset[2]
        microseconds -= expected_offset[3]

        total_seconds = (hours * 3600) + (minutes * 60) + seconds
        total_microseconds = (total_seconds * 10**6) + microseconds

        expected_molad = datetime(2015, 10, 13, 0, 0, 0, tzinfo=tz.UTC) + timedelta(microseconds=total_microseconds)
        self.assertEqual(calendar.molad_as_datetime(), expected_molad)

    def test_sof_zman_kiddush_levana_between_moldos(self):
        calendar = JewishCalendar(5776, 8, 1)
        next_month = JewishCalendar(5776, 9, 1)
        first_molad = calendar.molad_as_datetime()
        second_molad = next_month.molad_as_datetime()
        expected_offset = (second_molad - first_molad).total_seconds() * 10**6 / 2.0
        expected_time = first_molad + timedelta(microseconds=expected_offset)
        # round for floating microsecond precision inconsistency
        self.assertEqual(calendar.sof_zman_kiddush_levana_between_moldos().toordinal(), expected_time.toordinal())
