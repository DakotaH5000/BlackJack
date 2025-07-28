from gameHelpers import build_game_deck
from gameHelpers import calculate_totals
#Using the probabilites item of the distriubtion, create a voting system where each game state is calculated
#each deckCount votes with weighting on their respective choice

def determine_action_odds(probs, seen_cards, currentHand, dealerTotal):
    print(currentHand)
    player_value = calculate_totals(currentHand)
    print("det action")
    print(player_value)
    stored_actions = {}
    for i in range((22 - player_value), 10):
        stored_actions[i] = 0
    print("stored_actions")
    print(stored_actions)
    for i in range(len(probs)):
        #take prob, build a deck
        print(i)
        #deck = build_game_deck(i+1)
    return True