import unittest

from dateutil import parser, tz

from test import test_helper
from zmanim.util.geo_location import GeoLocation


class TestGeoLocation(unittest.TestCase):

    def test_GMT(self):
        gmt = GeoLocation.GMT()
        self.assertEqual(gmt.location_name, 'Greenwich, England')
        self.assertEqual(gmt.longitude, 0)
        self.assertEqual(gmt.latitude, 51.4772)
        self.assertTrue(gmt.time_zone._filename.endswith('/GMT'))
        self.assertEqual(gmt.elevation, 0)

    def test_latitude_numeric(self):
        geo = GeoLocation.GMT()
        geo.latitude = 33.3
        self.assertEqual(geo.latitude, 33.3)

    def test_latitude_cartography_north(self):
        geo = GeoLocation.GMT()
        geo.latitude = 41, 7, 5.17296, 'N'
        self.assertEqual(geo.latitude, 41.1181036)

    def test_latitude_cartography_south(self):
        geo = GeoLocation.GMT()
        geo.latitude = 41, 7, 5.17296, 'S'
        self.assertEqual(geo.latitude, -41.1181036)

    def test_longitude_numeric(self):
        geo = GeoLocation.GMT()
        geo.longitude = 23.4
        self.assertEqual(geo.longitude, 23.4)

    def test_longitude_cartography_east(self):
        geo = GeoLocation.GMT()
        geo.longitude = 41, 7, 5.17296, 'E'
        self.assertEqual(geo.longitude, 41.1181036)

    def test_longitude_cartography_west(self):
        geo = GeoLocation.GMT()
        geo.longitude = 41, 7, 5.17296, 'W'
        self.assertEqual(geo.longitude, -41.1181036)

    def test_time_zone_with_string(self):
        geo = GeoLocation.GMT()
        geo.time_zone = 'America/New_York'
        self.assertTrue(geo.time_zone._filename.endswith('/America/New_York'))

    def test_time_zone_with_timezone_object(self):
        geo = GeoLocation.GMT()
        geo.time_zone = tz.gettz('America/New_York')
        self.assertTrue(geo.time_zone._filename.endswith('/America/New_York'))

    def test_antimeridian_adjustment_for_gmt(self):
        geo = GeoLocation.GMT()
        self.assertEqual(geo.antimeridian_adjustment(), 0)

    def test_antimeridian_adjustment_for_standard_timezone(self):
        geo = GeoLocation.GMT()
        geo.time_zone = 'America/New_York'
        self.assertEqual(geo.antimeridian_adjustment(), 0)

    def test_antimeridian_adjustment_for_eastward_crossover(self):
        geo = test_helper.samoa()
        self.assertEqual(geo.antimeridian_adjustment(), -1)

    def test_antimeridian_adjustment_for_westward_crossover(self):
        geo = GeoLocation.GMT()
        geo.longitude = 179
        geo.time_zone = 'Etc/GMT+12'
        self.assertEqual(geo.antimeridian_adjustment(), 1)

    def test_local_mean_time_offset_for_gmt(self):
        geo = GeoLocation.GMT()
        self.assertEqual(geo.local_mean_time_offset(), 0)

    def test_local_mean_time_offset_on_center_meridian(self):
        geo = GeoLocation('Sample', 40, -75, 'America/New_York')
        self.assertEqual(geo.local_mean_time_offset(), 0)

    def test_local_mean_time_offset_east_of_center_meridian(self):
        geo = GeoLocation('Sample', 40, -74, 'America/New_York')
        self.assertEqual(geo.local_mean_time_offset(), 1 * 4 * GeoLocation.MINUTE_MILLIS)

    def test_local_mean_time_offset_west_of_center_meridian(self):
        geo = GeoLocation('Sample', 40, -76.25, 'America/New_York')
        self.assertEqual(geo.local_mean_time_offset(), -1.25 * 4 * GeoLocation.MINUTE_MILLIS)

    def test_standard_time_offset_for_gmt(self):
        geo = GeoLocation.GMT()
        self.assertEqual(geo.standard_time_offset(), 0)

    def test_standard_time_offset_for_standard_timezone(self):
        geo = GeoLocation.GMT()
        geo.time_zone = 'America/New_York'
        self.assertEqual(geo.standard_time_offset(), -5 * GeoLocation.HOUR_MILLIS)

    def test_time_zone_offset_at(self):
        expected = [('2017-03-12T06:30:00Z', 'US/Eastern', -5),
                    ('2017-03-12T07:00:00Z', 'US/Eastern', -4),
                    ('2017-03-12T09:30:00Z', 'US/Pacific', -8),
                    ('2017-03-12T10:00:00Z', 'US/Pacific', -7),
                    ('2017-03-23T23:30:00Z', 'Asia/Jerusalem', 2),
                    ('2017-03-24T00:00:00Z', 'Asia/Jerusalem', 3)]

        def test_entry(time, tz):
            geo = GeoLocation('Sample', 0, 0, tz)
            return time, tz, geo.time_zone_offset_at(parser.parse(time))

        for entry in expected:
            self.assertEqual(test_entry(entry[0], entry[1]), entry)


if __name__ == '__main__':
    unittest.main()