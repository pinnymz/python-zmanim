from geo_location import GeoLocation


def lakewood():
    return GeoLocation('Lakewood, NJ', 40.0721087, -74.2400243, 'America/New_York', elevation=15)


def samoa():
    return GeoLocation('Apia, Samoa', -13.8599098, -171.8031745, 'Pacific/Apia', elevation=1858)


def jerusalem():
    return GeoLocation('Jerusalem, Israel', 31.7781161, 35.233804, 'Asia/Jerusalem', elevation=740)


def los_angeles():
    return GeoLocation('Los Angeles, CA', 34.0201613, -118.6919095, 'America/Los_Angeles', elevation=71)


def tokyo():
    return GeoLocation('Tokyo, Japan', 35.6733227, 139.6403486, 'Asia/Tokyo', elevation=40)


def arctic_nunavut():
    return GeoLocation('Fort Conger, NU Canada', 81.7449398, -64.7945858, 'America/Toronto', elevation=127)


def basic_locations():
    return [lakewood(), jerusalem(), los_angeles(), tokyo(), arctic_nunavut(), samoa()]


def hooper_bay():
    return GeoLocation('Hooper Bay, Alaska', 61.520182, -166.1740437, 'America/Anchorage', elevation=8)


def daneborg():
    return GeoLocation('Daneborg, Greenland', 74.2999996, -20.2420877, 'America/Godthab', elevation=0)
