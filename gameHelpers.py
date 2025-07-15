def calculateTotals(hand):
    handTotal = 0
    subtract = False
    for card in hand:
        if card == 14:
            handTotal += 10
            subtract = True
        elif card < 10:
            handTotal += card
        elif card >= 10 < 14:
            handTotal += 10
    if subtract:
        if handTotal < 22:
            return handTotal
        return handTotal - 10
    else:
        return handTotal
