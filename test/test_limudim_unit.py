import unittest

from zmanim.limudim.unit import Unit


class TestLimudimUnit(unittest.TestCase):
    def test_str_for_a_primitive_unit(self):
        subject = Unit('berachos')
        self.assertEqual(str(subject), 'berachos')

    def test_str_for_a_paged_unit(self):
        subject = Unit(['berachos', 3])
        self.assertEqual(str(subject), 'berachos 3')

    def test_str_for_a_multi_level_unit_with_integers(self):
        subject = Unit(['berachos', 3, 5, 7, 4, 5])
        self.assertEqual(str(subject), 'berachos 3:5:7:4:5')

    def test_str_for_a_multi_level_unit_with_a_character(self):
        subject = Unit(['berachos', 'a'])
        self.assertEqual(str(subject), 'berachos a')

    def test_str_for_a_multi_level_unit_with_integer_and_then_a_character(self):
        subject = Unit(['berachos', 13, 'a'])
        self.assertEqual(str(subject), 'berachos 13a')

    def test_str_for_a_multi_level_unit_with_integer_and_then_a_character_and_rlm_marker(self):
        subject = Unit(['berachos', 13, u'a\u200f'])
        self.assertEqual(str(subject), u'berachos 13a\u200f')

    def test_str_for_a_multi_component_primitive_unit(self):
        subject = Unit('tazria', 'metzora')
        self.assertEqual(str(subject), 'tazria - metzora')

    def test_str_for_a_multi_component_integer_unit(self):
        subject = Unit(18, 25)
        self.assertEqual(str(subject), '18 - 25')

    def test_str_for_a_page_spanning_unit_with_similar_root_nodes(self):
        subject = Unit(['berachos', 3], ['berachos', 4])
        self.assertEqual(str(subject), 'berachos 3-4')

    def test_str_for_a_page_spanning_unit_with_different_root_nodes(self):
        subject = Unit(['berachos', 3], ['shabbos', 4])
        self.assertEqual(str(subject), 'berachos 3 - shabbos 4')

    def test_str_for_a_multi_level_spanning_unit_with_different_leaf_nodes(self):
        subject = Unit(['berachos', 3, 5], ['berachos', 3, 7])
        self.assertEqual(str(subject), 'berachos 3:5-7')

    def test_str_for_a_multi_level_spanning_unit_with_different_middle_nodes(self):
        subject = Unit(['berachos', 3, 5], ['berachos', 4, 1])
        self.assertEqual(str(subject), 'berachos 3:5-4:1')

    def test_str_for_a_multi_level_spanning_unit_with_different_root_nodes(self):
        subject = Unit(['berachos', 9, 1], ['peah', 1, 1])
        self.assertEqual(str(subject), 'berachos 9:1 - peah 1:1')

    def test_render_alters_rendering_using_passed_function(self):
        def sample_rendering_function(value):
            if isinstance(value, int):
                return value * 2
            else:
                return value.upper()

        subject = Unit(['berachos', 3])
        result = subject.render(sample_rendering_function)
        self.assertEqual(result, 'BERACHOS 6')


