from data.datatypes import cardsQuantity, suits

def calculateTotals(hand):
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
def buildGameDeck(numDecks):
    availableCards= []
    for key in cardsQuantity:
        for suit in suits:
                cardsQuantity[key][suit] *= numDecks
                for card in range(0,cardsQuantity[key][suit]):
                    availableCards.append(f'{key}{suit[0]}')
    return availableCards