from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from dateutil import tz

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.util.geo_location import GeoLocation


class JewishCalendar(JewishDate):
    SIGNIFICANT_DAYS = Enum('SignificantDays', 'erev_rosh_hashana rosh_hashana tzom_gedalyah erev_yom_kippur yom_kippur \
                                                erev_succos succos chol_hamoed_succos hoshana_rabbah shemini_atzeres simchas_torah \
                                                chanukah tenth_of_teves tu_beshvat \
                                                taanis_esther purim shushan_purim purim_katan shushan_purim_katan \
                                                erev_pesach pesach chol_hamoed_pesach pesach_sheni erev_shavuos shavuos \
                                                seventeen_of_tammuz tisha_beav tu_beav \
                                                yom_hashoah yom_hazikaron yom_haatzmaut yom_yerushalayim')

    def __init__(self, *args, **kwargs):
        in_israel = None
        if 'in_israel' in kwargs:
            in_israel = kwargs.pop('in_israel')
        if len(args) == 4:
            super(JewishCalendar, self).__init__(*args[:3], **kwargs)
            in_israel = args[3]
        else:
            super(JewishCalendar, self).__init__(*args, **kwargs)
        self.in_israel = False if in_israel is None else in_israel
        self.use_modern_holidays = False

    def __repr__(self):
        return "<%s in_israel=%r, gregorian_date=%r, jewish_date=%r, day_of_week=%r, molad_hours=%r, molad_minutes=%r, molad_chalakim=%r>" % \
               (self.__module__ + "." + self.__class__.__qualname__, self.in_israel, self.gregorian_date,
                self.jewish_date, self.day_of_week, self.molad_hours, self.molad_minutes, self.molad_chalakim)

    def significant_day(self) -> Optional[str]:
        return getattr(self, f'_{self.jewish_month_name()}_significant_day', None)()

    def is_assur_bemelacha(self) -> bool:
        return self.day_of_week == 7 or self.is_yom_tov_assur_bemelacha()

    def is_tomorrow_assur_bemelacha(self) -> bool:
        return self.day_of_week == 6 or self.is_erev_yom_tov() or self.is_erev_yom_tov_sheni()

    def has_candle_lighting(self) -> bool:
        return self.is_tomorrow_assur_bemelacha()

    def has_delayed_candle_lighting(self) -> bool:
        return self.day_of_week != 6 and self.has_candle_lighting() and self.is_assur_bemelacha()

    def is_yom_tov(self) -> bool:
        sd = self.significant_day()
        return sd is not None \
            and not sd.startswith('erev_') \
            and (not self.is_taanis() or sd == 'yom_kippur')

    def is_yom_tov_assur_bemelacha(self) -> bool:
        return self.significant_day() in ['pesach', 'shavuos', 'rosh_hashana', 'yom_kippur',
                                          'succos', 'shemini_atzeres', 'simchas_torah']

    def is_erev_yom_tov(self) -> bool:
        sd = self.significant_day()
        return sd is not None and (sd.startswith('erev_')
                                   or sd == 'hoshana_rabbah'
                                   or (sd == 'chol_hamoed_pesach' and self.jewish_day == 20))

    def is_yom_tov_sheni(self) -> bool:
        return ((self.jewish_month == 7 and self.jewish_day == 2)
                or (not self.in_israel and (
                    (self.jewish_month == 7 and self.jewish_day in [16, 23]) or
                    (self.jewish_month == 1 and self.jewish_day in [16, 22]) or
                    (self.jewish_month == 3 and self.jewish_day == 7)
                )))

    def is_erev_yom_tov_sheni(self) -> bool:
        return ((self.jewish_month == 7 and self.jewish_day == 1)
                or (not self.in_israel and (
                    (self.jewish_month == 7 and self.jewish_day in [15, 22]) or
                    (self.jewish_month == 1 and self.jewish_day in [15, 21]) or
                    (self.jewish_month == 3 and self.jewish_day == 6)
                )))

    def is_chol_hamoed(self) -> bool:
        sd = self.significant_day()
        return sd is not None and (sd.startswith('chol_hamoed_') or sd == 'hoshana_rabbah')

    def is_taanis(self) -> bool:
        return self.significant_day() in ['seventeen_of_tammuz', 'tisha_beav', 'tzom_gedalyah',
                                          'yom_kippur', 'tenth_of_teves', 'taanis_esther']

    def is_rosh_chodesh(self) -> bool:
        return self.jewish_day == 30 or (self.jewish_day == 1 and self.jewish_month != 7)

    def is_erev_rosh_chodesh(self) -> bool:
        return self.jewish_day == 29 and self.jewish_month != 6

    def is_chanukah(self) -> bool:
        return self.significant_day() == 'chanukah'

    def day_of_chanukah(self) -> Optional[int]:
        if not self.is_chanukah():
            return None

        if self.jewish_month_name() == 'kislev':
            return self.jewish_day - 24
        else:
            return self.jewish_day + (5 if self.is_kislev_short() else 6)

    def day_of_omer(self) -> Optional[int]:
        month_name = self.jewish_month_name()
        if month_name == 'nissan':
            return self.jewish_day - 15 if self.jewish_day > 15 else None
        elif month_name == 'iyar':
            return self.jewish_day + 15
        elif month_name == 'sivan':
            return self.jewish_day + 44 if self.jewish_day < 6 else None
        else:
            return None

    def molad_as_datetime(self) -> datetime:
        m = self.molad()
        location_name = 'Jerusalem, Israel'
        latitude = 31.778  # Har Habayis latitude
        longitude = 35.2354  # Har Habayis longitude
        zone = tz.gettz('Asia/Jerusalem')

        geo = GeoLocation(location_name, latitude, longitude, zone)
        seconds = m.molad_chalakim * 10 / 3.0
        seconds, microseconds = divmod(seconds * 10**6, 10**6)
        # molad as local mean time
        time = datetime(m.gregorian_year, m.gregorian_month, m.gregorian_day,
                        m.molad_hours, m.molad_minutes, int(seconds), int(microseconds),
                        tzinfo=tz.gettz('Etc/GMT-2'))
        # molad as Jerusalem standard time
        micro_offset = geo.local_mean_time_offset() * 1000
        time -= timedelta(microseconds=micro_offset)
        # molad as UTC
        return time.astimezone(tz.UTC)

    def techilas_zman_kiddush_levana_3_days(self) -> datetime:
        return self.molad_as_datetime() + timedelta(3)

    def techilas_zman_kiddush_levana_7_days(self) -> datetime:
        return self.molad_as_datetime() + timedelta(7)

    def sof_zman_kiddush_levana_between_moldos(self) -> datetime:
        half_molad_in_seconds = self.CHALAKIM_PER_MONTH * 10 / 6.0
        return self.molad_as_datetime() + timedelta(microseconds=half_molad_in_seconds * 10**6)

    def sof_zman_kiddush_levana_15_days(self) -> datetime:
        return self.molad_as_datetime() + timedelta(15)

    def _nissan_significant_day(self) -> Optional[str]:
        pesach = [15, 21]
        if not self.in_israel:
            pesach += [16, 22]

        if self.jewish_day == 14:
            return 'erev_pesach'
        elif self.jewish_day in pesach:
            return 'pesach'
        elif self.jewish_day in range(16,21):
            return 'chol_hamoed_pesach'
        elif self.use_modern_holidays:
            if (self.jewish_day == 26 and self.day_of_week == 5) \
                    or (self.jewish_day == 27 and self.day_of_week not in [1, 6]) \
                    or (self.jewish_day == 28 and self.day_of_week == 2):
                return 'yom_hashoah'

    def _iyar_significant_day(self) -> Optional[str]:
        if self.jewish_day == 14:
            return 'pesach_sheni'
        elif self.use_modern_holidays:
            # Note that this logic follows the current rules, which were last revised in 5764.
            # The calculations for years prior may not reflect the actual dates observed at that time.
            if (self.jewish_day in [2, 3] and self.day_of_week == 4) \
                    or (self.jewish_day == 4 and self.day_of_week == 3) \
                    or (self.jewish_day == 5 and self.day_of_week == 2):
                return 'yom_hazikaron'
            elif (self.jewish_day in [3, 4] and self.day_of_week == 5) \
                    or (self.jewish_day == 5 and self.day_of_week == 4) \
                    or (self.jewish_day == 6 and self.day_of_week == 3):
                return 'yom_haatzmaut'
            elif self.jewish_day == 28:
                return 'yom_yerushalayim'

    def _sivan_significant_day(self) -> Optional[str]:
        shavuos = [6]
        if not self.in_israel:
            shavuos += [7]

        if self.jewish_day == 5:
            return 'erev_shavuos'
        elif self.jewish_day in shavuos:
            return 'shavuos'

    def _tammuz_significant_day(self) -> Optional[str]:
        if (self.jewish_day == 17 and self.day_of_week != 7) \
                or (self.jewish_day == 18 and self.day_of_week == 1):
            return 'seventeen_of_tammuz'

    def _av_significant_day(self) -> Optional[str]:
        if (self.jewish_day == 9 and self.day_of_week != 7) \
                or (self.jewish_day == 10 and self.day_of_week == 1):
            return 'tisha_beav'
        elif self.jewish_day == 15:
            return 'tu_beav'

    def _elul_significant_day(self) -> Optional[str]:
        if self.jewish_day == 29:
            return 'erev_rosh_hashana'

    def _tishrei_significant_day(self) -> Optional[str]:
        succos = [15]
        if not self.in_israel:
            succos += [16]

        if self.jewish_day in [1, 2]:
            return 'rosh_hashana'
        elif (self.jewish_day == 3 and self.day_of_week != 7) \
                or (self.jewish_day == 4 and self.day_of_week == 1):
            return 'tzom_gedalyah'
        elif self.jewish_day == 9:
            return 'erev_yom_kippur'
        elif self.jewish_day == 10:
            return 'yom_kippur'
        elif self.jewish_day == 14:
            return 'erev_succos'
        elif self.jewish_day in succos:
            return 'succos'
        elif self.jewish_day in range(16,21):
            return 'chol_hamoed_succos'
        elif self.jewish_day == 21:
            return 'hoshana_rabbah'
        elif self.jewish_day == 22:
            return 'shemini_atzeres'
        elif self.jewish_day == 23 and not self.in_israel:
            return 'simchas_torah'

    def _cheshvan_significant_day(self) -> None:
        return None

    def _kislev_significant_day(self) -> Optional[str]:
        if self.jewish_day >= 25:
            return 'chanukah'

    def _teves_significant_day(self) -> Optional[str]:
        chanukah = [1,2]
        if self.is_kislev_short():
            chanukah += [3]

        if self.jewish_day in chanukah:
            return 'chanukah'
        elif self.jewish_day == 10:
            return 'tenth_of_teves'

    def _shevat_significant_day(self) -> Optional[str]:
        if self.jewish_day == 15:
            return 'tu_beshvat'

    def _adar_significant_day(self) -> Optional[str]:
        if self.is_jewish_leap_year():
            if self.jewish_day == 14:
                return 'purim_katan'
            elif self.jewish_day == 15:
                return 'shushan_purim_katan'
        else:
            return self._purim_significant_day()

    def _adar_ii_significant_day(self) -> Optional[str]:
        return self._purim_significant_day()

    def _purim_significant_day(self) -> Optional[str]:
        if (self.jewish_day == 13 and self.day_of_week != 7) \
                or (self.jewish_day == 11 and self.day_of_week == 5):
            return 'taanis_esther'
        elif self.jewish_day == 14:
            return 'purim'
        elif self.jewish_day == 15:
            return 'shushan_purim'