import unittest
from datetime import date, timedelta

from dateutil import parser

from test import test_helper
from zmanim.zmanim_calendar import ZmanimCalendar


class TestZmanimCalendar(unittest.TestCase):
    def test_hanetz(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.hanetz(), calendar.sea_level_sunrise())

    def test_shkia(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.shkia(), calendar.sea_level_sunset())

    def test_tzais(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.tzais().replace(microsecond=0).isoformat(), "2017-10-17T18:54:29-04:00")

    def test_tzais_with_custom_degree_offset(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.tzais({'degrees': 19.8}).replace(microsecond=0).isoformat(), "2017-10-17T19:53:34-04:00")

    def test_tzais_with_custom_minute_offset(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.tzais({'offset': 60}).replace(microsecond=0).isoformat(), "2017-10-17T19:13:58-04:00")

    def test_tzais_with_custom_temporal_minute_offset(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.tzais({'zmanis_offset': 90}).replace(microsecond=0).isoformat(), "2017-10-17T19:36:59-04:00")

    def test_tzais_72(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.tzais_72().replace(microsecond=0).isoformat(), "2017-10-17T19:25:58-04:00")

    def test_alos(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.alos().replace(microsecond=0).isoformat(), "2017-10-17T05:49:30-04:00")

    def test_alos_with_custom_degree_offset(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.alos({'degrees': 19.8}).replace(microsecond=0).isoformat(), "2017-10-17T05:30:07-04:00")

    def test_alos_with_custom_minute_offset(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.alos({'offset': 60}).replace(microsecond=0).isoformat(), "2017-10-17T06:09:51-04:00")

    def test_alos_with_custom_temporal_minute_offset(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.alos({'zmanis_offset': 90}).replace(microsecond=0).isoformat(), "2017-10-17T05:46:50-04:00")

    def test_alos_72(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.alos_72().replace(microsecond=0).isoformat(), "2017-10-17T05:57:51-04:00")

    def test_chatzos(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.chatzos().replace(microsecond=0).isoformat(), "2017-10-17T12:41:55-04:00")

    def test_sof_zman_shma(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        day_start = calendar.sunrise_offset_by_degrees(96)
        day_end = calendar.sunset_offset_by_degrees(96)
        self.assertEqual(calendar.sof_zman_shma(day_start, day_end).replace(microsecond=0).isoformat(), "2017-10-17T09:42:10-04:00")

    def test_sof_zman_shma_gra(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.sof_zman_shma_gra().replace(microsecond=0).isoformat(), "2017-10-17T09:55:53-04:00")

    def test_sof_zman_shma_mga(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.sof_zman_shma_mga().replace(microsecond=0).isoformat(), "2017-10-17T09:19:53-04:00")

    def test_sof_zman_tfila(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        day_start = calendar.sunrise_offset_by_degrees(96)
        day_end = calendar.sunset_offset_by_degrees(96)
        self.assertEqual(calendar.sof_zman_tfila(day_start, day_end).replace(microsecond=0).isoformat(), "2017-10-17T10:42:05-04:00")

    def test_sof_zman_tfila_gra(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.sof_zman_tfila_gra().replace(microsecond=0).isoformat(), "2017-10-17T10:51:14-04:00")

    def test_sof_zman_tfila_mga(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.sof_zman_tfila_mga().replace(microsecond=0).isoformat(), "2017-10-17T10:27:14-04:00")

    def test_mincha_gedola(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.mincha_gedola().replace(microsecond=0).isoformat(), "2017-10-17T13:09:35-04:00")

    def test_mincha_ketana(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.mincha_ketana().replace(microsecond=0).isoformat(), "2017-10-17T15:55:37-04:00")

    def test_plag_hamincha(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.plag_hamincha().replace(microsecond=0).isoformat(), "2017-10-17T17:04:48-04:00")

    def test_candle_lighting(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.candle_lighting().replace(microsecond=0).isoformat(), "2017-10-17T17:55:58-04:00")

    def test_shaah_zmanis(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        day_start = calendar.sunrise_offset_by_degrees(96)
        day_end = calendar.sunset_offset_by_degrees(96)
        self.assertEqual(int(calendar.shaah_zmanis(day_start, day_end)), 3594499)

    def test_shaah_zmanis_gra(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(int(calendar.shaah_zmanis_gra()), 3320608)

    def test_shaah_zmanis_mga(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(int(calendar.shaah_zmanis_mga()), 4040608)

    def test_shaah_zmanis_by_degrees_and_offset_with_degrees(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(int(calendar.shaah_zmanis_by_degrees_and_offset(6, 0)), 3594499)

    def test_shaah_zmanis_by_degrees_and_offset_with_offset(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(int(calendar.shaah_zmanis_by_degrees_and_offset(0, 72)), 4040608)

    def test_shaah_zmanis_by_degrees_and_offset_with_both_degrees_and_offset(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(int(calendar.shaah_zmanis_by_degrees_and_offset(6, 72)), 4314499)

    def test_hanetz_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.hanetz(), calendar.sunrise())

    def test_shkia_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.shkia(), calendar.sunset())

    def test_tzais_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.tzais().replace(microsecond=0).isoformat(), "2017-10-17T18:54:29-04:00")

    def test_tzais_with_custom_degree_offset_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.tzais({'degrees': 19.8}).replace(microsecond=0).isoformat(), "2017-10-17T19:53:34-04:00")

    def test_tzais_with_custom_minute_offset_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.tzais({'offset': 60}).replace(microsecond=0).isoformat(), "2017-10-17T19:14:38-04:00")

    def test_tzais_with_custom_temporal_minute_offset_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.tzais({'zmanis_offset': 90}).replace(microsecond=0).isoformat(), "2017-10-17T19:37:49-04:00")

    def test_tzais_72_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.tzais_72().replace(microsecond=0).isoformat(), "2017-10-17T19:26:38-04:00")

    def test_alos_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.alos().replace(microsecond=0).isoformat(), "2017-10-17T05:49:30-04:00")

    def test_alos_with_custom_degree_offset_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.alos({'degrees': 19.8}).replace(microsecond=0).isoformat(), "2017-10-17T05:30:07-04:00")

    def test_alos_with_custom_minute_offset_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.alos({'offset': 60}).replace(microsecond=0).isoformat(), "2017-10-17T06:09:11-04:00")

    def test_alos_with_custom_temporal_minute_offset_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.alos({'zmanis_offset': 90}).replace(microsecond=0).isoformat(), "2017-10-17T05:46:00-04:00")

    def test_alos_72_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.alos_72().replace(microsecond=0).isoformat(), "2017-10-17T05:57:11-04:00")

    def test_chatzos_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.chatzos().replace(microsecond=0).isoformat(), "2017-10-17T12:41:55-04:00")

    def test_sof_zman_shma_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        day_start = calendar.sunrise_offset_by_degrees(96)
        day_end = calendar.sunset_offset_by_degrees(96)
        self.assertEqual(calendar.sof_zman_shma(day_start, day_end).replace(microsecond=0).isoformat(), "2017-10-17T09:42:10-04:00")

    def test_sof_zman_shma_gra_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.sof_zman_shma_gra().replace(microsecond=0).isoformat(), "2017-10-17T09:55:33-04:00")

    def test_sof_zman_shma_mga_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.sof_zman_shma_mga().replace(microsecond=0).isoformat(), "2017-10-17T09:19:33-04:00")

    def test_sof_zman_tfila_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        day_start = calendar.sunrise_offset_by_degrees(96)
        day_end = calendar.sunset_offset_by_degrees(96)
        self.assertEqual(calendar.sof_zman_tfila(day_start, day_end).replace(microsecond=0).isoformat(), "2017-10-17T10:42:05-04:00")

    def test_sof_zman_tfila_gra_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.sof_zman_tfila_gra().replace(microsecond=0).isoformat(), "2017-10-17T10:51:00-04:00")

    def test_sof_zman_tfila_mga_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.sof_zman_tfila_mga().replace(microsecond=0).isoformat(), "2017-10-17T10:27:00-04:00")

    def test_mincha_gedola_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.mincha_gedola().replace(microsecond=0).isoformat(), "2017-10-17T13:09:38-04:00")

    def test_mincha_ketana_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.mincha_ketana().replace(microsecond=0).isoformat(), "2017-10-17T15:56:00-04:00")

    def test_plag_hamincha_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.plag_hamincha().replace(microsecond=0).isoformat(), "2017-10-17T17:05:19-04:00")

    def test_candle_lighting_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(calendar.candle_lighting().replace(microsecond=0).isoformat(), "2017-10-17T17:55:58-04:00")

    def test_shaah_zmanis_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        day_start = calendar.sunrise_offset_by_degrees(96)
        day_end = calendar.sunset_offset_by_degrees(96)
        self.assertEqual(int(calendar.shaah_zmanis(day_start, day_end)), 3594499)

    def test_shaah_zmanis_gra_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(int(calendar.shaah_zmanis_gra()), 3327251)

    def test_shaah_zmanis_mga_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(int(calendar.shaah_zmanis_mga()), 4047251)

    def test_shaah_zmanis_by_degrees_and_offset_with_degrees_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(int(calendar.shaah_zmanis_by_degrees_and_offset(6, 0)), 3594499)

    def test_shaah_zmanis_by_degrees_and_offset_with_offset_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(int(calendar.shaah_zmanis_by_degrees_and_offset(0, 72)), 4047251)

    def test_shaah_zmanis_by_degrees_and_offset_with_both_degrees_and_offset_using_elevation(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        calendar.use_elevation = True
        self.assertEqual(int(calendar.shaah_zmanis_by_degrees_and_offset(6, 72)), 4314499)
        
    def test_assur_bemelacha_for_standard_day(self):
        date = '2017-10-17'
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=parser.parse(date))
        self.assertFalse(calendar.is_assur_bemelacha(calendar.shkia() - timedelta(seconds=2)))
        self.assertFalse(calendar.is_assur_bemelacha(calendar.tzais() - timedelta(seconds=2)))
        self.assertFalse(calendar.is_assur_bemelacha(calendar.tzais() + timedelta(seconds=2)))

    def test_assur_bemelacha_for_issur_melacha_day(self):
        date = '2017-10-21'
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=parser.parse(date))
        self.assertTrue(calendar.is_assur_bemelacha(calendar.shkia() - timedelta(seconds=2)))
        self.assertTrue(calendar.is_assur_bemelacha(calendar.tzais() - timedelta(seconds=2)))
        self.assertFalse(calendar.is_assur_bemelacha(calendar.tzais() + timedelta(seconds=2)))

    def test_assur_bemelacha_for_issur_melacha_day_with_custom_tzais_time(self):
        date = '2017-10-21'
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=parser.parse(date))
        tzais = calendar.tzais_72()
        self.assertTrue(calendar.is_assur_bemelacha(tzais - timedelta(seconds=2), tzais))
        self.assertFalse(calendar.is_assur_bemelacha(tzais + timedelta(seconds=2), tzais))

    def test_assur_bemelacha_for_issur_melacha_day_with_custom_tzais_rule(self):
        date = '2017-10-21'
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=parser.parse(date))
        tzais = calendar.tzais({'degrees': 11.5})
        self.assertTrue(calendar.is_assur_bemelacha(tzais - timedelta(seconds=2), {'degrees': 11.5}))
        self.assertFalse(calendar.is_assur_bemelacha(tzais + timedelta(seconds=2), {'degrees': 11.5}))

    def test_assur_bemelacha_prior_to_issur_melacha_day(self):
        date = '2017-10-20'
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=parser.parse(date))
        self.assertFalse(calendar.is_assur_bemelacha(calendar.shkia() - timedelta(seconds=2)))
        self.assertTrue(calendar.is_assur_bemelacha(calendar.tzais() - timedelta(seconds=2)))
        self.assertTrue(calendar.is_assur_bemelacha(calendar.tzais() + timedelta(seconds=2)))

    def test_assur_bemelacha_on_first_of_two_issur_melacha_days(self):
        date = '2018-03-31'  # first day of pesach
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=parser.parse(date))
        self.assertTrue(calendar.is_assur_bemelacha(calendar.shkia() - timedelta(seconds=2)))
        self.assertTrue(calendar.is_assur_bemelacha(calendar.tzais() - timedelta(seconds=2)))
        self.assertTrue(calendar.is_assur_bemelacha(calendar.tzais() + timedelta(seconds=2)))

    def test_assur_bemelacha_on_first_of_single_issur_melacha_in_israel(self):
        date = '2018-03-31'  # first day of pesach
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=parser.parse(date))
        self.assertTrue(calendar.is_assur_bemelacha(calendar.tzais() - timedelta(seconds=2), in_israel=True))
        self.assertFalse(calendar.is_assur_bemelacha(calendar.tzais() + timedelta(seconds=2), in_israel=True))

    def test_assur_bemelacha_on_first_of_two_issur_melacha_days_in_israel(self):
        date = '2018-05-19'  # Shabbos before Shavuos
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=parser.parse(date))
        self.assertTrue(calendar.is_assur_bemelacha(calendar.tzais() - timedelta(seconds=2), in_israel=True))
        self.assertTrue(calendar.is_assur_bemelacha(calendar.tzais() + timedelta(seconds=2), in_israel=True))


if __name__ == '__main__':
    unittest.main()