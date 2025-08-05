from collections import Counter
from gameHelpers import build_game_deck
from gameHelpers import calculate_totals, trim_suit
#Using the probabilites item of the distriubtion, create a voting system where each game state is calculated
#each deckCount votes with weighting on their respective choice

def determine_action_odds(probs, seen_cards, currentHand, dealer_card):
    player_value = calculate_totals(currentHand)
    print(player_value)
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

            #calculate cards that could cause a bust
            card_totals = dict(sorted(Counter(trim_suit(deck.copy())).items()))
            dealer_estimate = dealer_expected_value(cards_in_deck, card_totals) + dealer_card
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
    print(f'hit matrix for {currentHand}, {hit_matrix}')
    for i in range(0, len(decision_matrix)):
        if hit_matrix[i] == 0 or hit_matrix[i] < 0.50:
             voteMatrix[0] += decision_matrix[i]
        if hit_matrix[i] >= 0.50:
             voteMatrix[1] += decision_matrix[i]
    print(stored_actions)
    print(currentHand)
    print(cards_in_deck)
    print(voteMatrix)
    get_key_of_best_odds = max(voteMatrix, key=voteMatrix.get)
    return get_key_of_best_odds

#This function does not account for the discrepancy in the fact there is a hidden dealer card.
#It calculates the odds with the card in the deck given the card is unknown
def dealer_expected_value(num_cards, card_counts):
    card_total = 0 
    for key,value in card_counts.items():
        if int(key) <= 10:
            card_total = card_total + (int(key) * int(value))
        if 10 < int(key) < 14:
            card_total = card_total + ( 10 * int(value))
        if int(key) == 14:
            #Probably a better solution to this problem which can be further researched but as an expected value,
            #aces are either high or low, use intermediate value for estimation. 
            #First hunch for tweaking is find ratio of H/L ace usage and adjust value according. 
            card_total = card_total + (6 * int(value))
    return card_total/num_cards

