import unittest
from datetime import date

from test import test_helper
from zmanim.zmanim_calendar import ZmanimCalendar


class TestZmanimCalendar(unittest.TestCase):
    def test_tzais(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.tzais().replace(microsecond=0).isoformat(), "2017-10-17T18:54:29-04:00")

    def test_tzais_72(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.tzais_72().replace(microsecond=0).isoformat(), "2017-10-17T19:25:58-04:00")

    def test_alos(self):
        calendar = ZmanimCalendar(geo_location=test_helper.lakewood(), date=date(2017, 10, 17))
        self.assertEqual(calendar.alos().replace(microsecond=0).isoformat(), "2017-10-17T05:49:30-04:00")

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


if __name__ == '__main__':
    unittest.main()