import unittest
from main import trimSuit

class TestTrimSuit(unittest.TestCase):
    def test_all_string_cards(self):
        self.assertEqual(trimSuit(['14S', '10H', '3D']), [14, 10, 3])

    def test_mixed_types(self):
        self.assertEqual(trimSuit([14, 5, '3H']), [14, 5, 3])
        self.assertEqual(trimSuit(['14S', 7, '9C']), [14, 7, 9])

    def test_no_suits(self):
        self.assertEqual(trimSuit([14, 5, 3]), [14, 5, 3])

    def test_empty_list(self):
        self.assertEqual(trimSuit([]), [])

    def test_single_string_card(self):
        self.assertEqual(trimSuit(['10D']), [10])

    def test_single_int(self):
        self.assertEqual(trimSuit([7]), [7])

    def test_invalid_strings(self):
        # This will raise ValueError if the substring before suit is not an int
        with self.assertRaises(ValueError):
            trimSuit(['XH', '9D'])

    def test_non_string_non_int(self):
        # Objects that are not strings or ints remain unchanged (no conversion)
        hand = [14, 5.5, '7C', None]
        trimmed = trimSuit(hand)
        self.assertEqual(trimmed, [14, 5.5, 7, None])

if __name__ == '__main__':
    unittest.main()
