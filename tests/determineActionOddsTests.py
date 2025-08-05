from calculatedOddsActions import determine_action_odds
import unittest


class TestDetermineActionOdds(unittest.TestCase):
    #probs = [0.37256492, 0.12114484, 0.08547927, 0.07211444, 0.06520754, 0.0610076, 0.05818956, 0.05616976, 0.05465197, 0.05347011]
    #seen_cards = {'6H': 1, '5C': 1, '13D': 1, '10H': 1, '3S': 1, '10D': 1, '2C': 1, '6S': 1, '13H': 1, '4D': 1, '3D': 1} 
    #hand = [13, 4]
    #dealerCard = 3
    

    def test_runs(self):
        probs = [0.37256492, 0.12114484, 0.08547927, 0.07211444, 0.06520754, 0.0610076, 0.05818956, 0.05616976, 0.05465197, 0.05347011]
        seen_cards = {'6H': 1, '5C': 1, '13D': 1, '10H': 1, '3S': 1, '10D': 1, '2C': 1, '6S': 1, '13H': 1, '4D': 1, '3D': 1} 
        hand = [13, 4]
        dealerCard = 3
        value = determine_action_odds(probs,seen_cards, hand, dealerCard)
        self.assertIsNotNone(value)

    def test_returns_0(self):
        probs = [0.37256492, 0.12114484, 0.08547927, 0.07211444, 0.06520754, 0.0610076, 0.05818956, 0.05616976, 0.05465197, 0.05347011]
        seen_cards = {'6H': 1, '5C': 1, '13D': 1, '10H': 1, '3S': 1, '10D': 1, '2C': 1, '6S': 1, '13H': 1, '7D': 1, '3D': 1} 
        hand = [13, 7]
        dealerCard = 3
        value = determine_action_odds(probs,seen_cards, hand, dealerCard)
        self.assertEqual(value,0)

    #13H turned into 6D to force a hit scenario
    def test_returns_1(self):
        probs = [0.37256492, 0.12114484, 0.08547927, 0.07211444, 0.06520754, 0.0610076, 0.05818956, 0.05616976, 0.05465197, 0.05347011]
        seen_cards = {'6H': 1, '5C': 1, '13D': 1, '10H': 1, '3S': 1, '10D': 1, '2C': 1, '6S': 1, '6D': 1, '4D': 1, '3D': 1} 
        hand = [6, 4]
        dealerCard = 3
        value = determine_action_odds(probs,seen_cards, hand, dealerCard)
        self.assertEqual(value,1)

if __name__ == '__main__':
    unittest.main()
