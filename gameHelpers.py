from data.datatypes import cardsQuantity, suits

def calculate_totals(hand):
    handTotal = 0
    subtract = False
    for card in hand:
        if card == 14:
            handTotal += 11
            subtract = True
        elif card < 10:
            handTotal += card
        elif 10 <= card < 14:
            handTotal += 10
    if subtract:
        ace_count = hand.count(14)
        for ace_count in range(ace_count):
            if handTotal > 21:
                handTotal -= 10
        return handTotal
    else:
        return handTotal


#Set the number of cards properly
def build_game_deck(numDecks):
    availableCards = []
    for key in cardsQuantity:
        for suit in suits:
            for _ in range(numDecks):
                availableCards.append(f'{key}{suit[0]}')
    return availableCards


def trim_suit(hand):
    for i in range(len(hand)):
        try:
            if isinstance(hand[i], str):
                hand[i] = int(hand[i][:-1])  # Remove last character (suit)
        #These errors should never be raised unless something is crazy broken
        except ValueError:
                raise ValueError(f"Cannot convert card value '{hand[i][:-1]}' to int")
        except Exception as e:
                # Catch unexpected errors and re-raise with context
                raise RuntimeError(f"Error processing card '{hand[i]}': {e}")

    return hand