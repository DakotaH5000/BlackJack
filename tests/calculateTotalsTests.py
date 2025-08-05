from gameHelpers import calculateTotals
import unittest

class TestCalculateTotals(unittest.TestCase):
    def test_no_aces(self):
        self.assertEqual(calculateTotals([2, 3, 4]), 9)
        self.assertEqual(calculateTotals([10, 11]), 20)
        self.assertEqual(calculateTotals([9, 10]), 19)
        self.assertEqual(calculateTotals([13,11]), 20)
        self.assertEqual(calculateTotals([13,11,5]), 25)

    def test_with_ace_under_21(self):
        self.assertEqual(calculateTotals([14, 5]), 16)  # Ace as 11
        self.assertEqual(calculateTotals([14, 6, 4]), 21)  # Ace as 11

    def test_with_ace_over_21(self):
        self.assertEqual(calculateTotals([14, 10, 10]), 21)  # Ace drops to 1
        self.assertEqual(calculateTotals([14, 9, 4]), 14)    # Ace drops to 1

    def test_multiple_aces(self):
        self.assertEqual(calculateTotals([14, 14, 4]), 16)  # Only one ace reduced
        self.assertEqual(calculateTotals([14, 14, 10]), 12)  # Only one ace reduced
        self.assertEqual(calculateTotals([14,14, 10, 9]), 21) # Reduce two aces 
        self.assertEqual(calculateTotals([14, 14, 8, 6, 5]), 21) # Reduce two aces 

    def test_exact_21_with_ace(self):
        self.assertEqual(calculateTotals([14, 10]), 21)  # Ace as 11
        self.assertEqual(calculateTotals([14, 7, 3]), 21)  # Ace as 11

if __name__ == '__main__':
    unittest.main()
