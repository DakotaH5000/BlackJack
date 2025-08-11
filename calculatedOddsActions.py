from collections import Counter
from gameHelpers import build_game_deck
from gameHelpers import calculate_totals, trim_suit
from calculate_actions import calculate_stand, calculate_hit, calculate_split, calculate_double
from data_helpers import get_expected_value
#Using the probabilites item of the distriubtion, create a voting system where each game state is calculated
#each deckCount votes with weighting on their respective choice

def determine_action_odds(probs, seen_cards, currentHand, dealer_card):


    player_value = calculate_totals(currentHand)
    if player_value == 21: 
         return [0,0,0,0]

    if player_value == 21:
         return 0
    
    decision_matrix = probs
    hit_matrix = [0] * len(probs)
    stored_actions = {}
    for i in range((22 - player_value), 14):
        stored_actions[i] = 0

    min_decks = int(max(seen_cards.values()))
    for i in range(min_decks, len(probs)):
        if probs[i] > 0.0:
                #take prob, build a deck
            deck = build_game_deck(i+1)

            #set deck up for current known game state
            for key, count in seen_cards.items():
                for _ in range(count):
                    if key in deck:
                        deck.remove(key)
            cards_in_deck = len(deck)
            card_totals = dict(sorted(Counter(trim_suit(deck.copy())).items()))

            game_options = [
                calculate_stand(player_value, card_totals, dealer_card, cards_in_deck),
                calculate_hit(player_value, card_totals, dealer_card, cards_in_deck),
                calculate_split(player_value, card_totals, dealer_card, cards_in_deck),
                calculate_double(player_value, card_totals, dealer_card, cards_in_deck)
            ]

            print(game_options)

            #calculate cards that could cause a bust
            dealer_estimate = get_expected_value(cards_in_deck, card_totals) + dealer_card
            cards_resulting_in_bust = 0

            for rank in range(2,14):
                pre_determined_action = stored_actions.get(rank)
                if pre_determined_action is not None:
                    if int(pre_determined_action) == 0:
                        cards_resulting_in_bust += int(card_totals[rank])
            if (cards_resulting_in_bust) /cards_in_deck >= 0.5:
                    hit_matrix[i] = 0
            else:
                    chance_not_bust = (1 - (cards_resulting_in_bust / cards_in_deck))
                    hit_matrix[i] = chance_not_bust
            #wrap above logic in a function to later return the decison matrix
            #if player should hit and is currently losing what is Σall paths
            if player_value < dealer_estimate:
                 pass

    #Needs additional logic to check for recursive hits that may be needed
    voteMatrix = {0:0,1:0}

    for i in range(0, len(decision_matrix)):
        if hit_matrix[i] == 0 or hit_matrix[i] < 0.50:
             voteMatrix[0] += decision_matrix[i]
        if hit_matrix[i] >= 0.50:
             voteMatrix[1] += decision_matrix[i]
    get_key_of_best_odds = max(voteMatrix, key=voteMatrix.get)
    print(get_key_of_best_odds)
    return get_key_of_best_odds
