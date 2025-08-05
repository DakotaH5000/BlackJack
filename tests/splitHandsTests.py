from main import splitHands
from data.gameDeck import gameDeck
import unittest
import random


class TestSplitHands(unittest.TestCase):

    def setUp(self):
        # Set a fixed seed for reproducibility
        random.seed(42)

        # Setup a test game deck with 52 cards
        self.fullDeck = gameDeck
        print(f'gameDeck: {self.fullDeck}')

    def test_split_hands_removes_cards(self):
        hands = ['14S', '14C']  # original pair to be split
        gameCards = self.fullDeck.copy()

        # Remove initial hands from the deck
        gameCards.remove('14S')
        gameCards.remove('14C')
        self.assertEqual(len(gameCards), 50)
        originalLength = len(gameCards)  # should be 50

        split = splitHands(hands, gameCards)

        # Assert each hand has 2 cards
        self.assertEqual(len(split[0]), 2)
        self.assertEqual(len(split[1]), 2)

        print(split)
        # Assert original cards are still in first position
        self.assertEqual(split[0][0], '14S')
        self.assertEqual(split[1][0], '14C')

        # Check that the new cards were removed from the gameCards
        drawn_cards = [split[0][1], split[1][1]]
        for card in drawn_cards:
            self.assertNotIn(card, gameCards)

        # Confirm exactly 2 cards were removed
        self.assertEqual(len(gameCards), originalLength - 2)

        # No duplicate cards across both hands
        all_cards = split[0] + split[1]
        self.assertEqual(len(set(all_cards)), 4)

    def test_repeatable_results_with_seed(self):
        random.seed(42)
        hands = ['14S', '14C']
        gameCards = self.fullDeck.copy()
        gameCards.remove('14S')
        gameCards.remove('14C')

        split1 = splitHands(hands, gameCards.copy())
        random.seed(42)
        split2 = splitHands(hands, gameCards.copy())
        self.assertEqual(split1, split2)

    def test_added_back_to_deck(self):
        random.seed(42)
        hands = [['14S', '14C']]
        hands.append(['13S', '13C'])  # Add a King hand
        hands.append(['12H', '11D'])  # Add Queen + Jack
        hands.append(['10S', '9H']) 
        gameCards = self.fullDeck.copy()
        gameCards.remove('14S')
        gameCards.remove('14C')
        split1 = splitHands(hands[0], gameCards.copy())
        for hand in split1:
            hands.append(hand)
        hands.pop(0)

        self.assertEqual(len(hands), 5)
        self.assertEqual(hands[-2], ['14S', '4D'])
        self.assertEqual(hands[-1], ['14C', '12C'])

if __name__ == "__main__":
    unittest.main()