import unittest
import tempfile
from fixtures import delivery
from delivery import members, read_member
from dialects import profile
from csv_probe import parse_known
from preview import preview_delivery


class TextTests(unittest.TestCase):
    def test_multiline_and_leading_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            result = preview_delivery(delivery('west', multiline=True), 'west', directory)
            self.assertEqual(result['accepted'][0]['member_id'], '00017')
            self.assertEqual(result['accepted'][0]['amount'], '1,250.00')
            self.assertIn('\n', result['accepted'][0]['note'])

    def test_path_classification_does_not_extract(self):
        rows = list(members(delivery(unsafe=True)))
        self.assertFalse(rows[-1]['path_safe'])
        self.assertTrue(rows[0]['path_safe'])

    def test_member_limit_and_unknown_profile(self):
        with self.assertRaises(ValueError):
            read_member(delivery(), 0, limit=2)
        with self.assertRaises(ValueError):
            profile('unknown')

    def test_wrong_shape_is_not_a_partial_success(self):
        with self.assertRaises(ValueError):
            parse_known(b'member_id,amount\n0001,1,extra\n', profile('east'))
