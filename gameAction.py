#add double down and split logic
def determinePlayerAction(cards, dealerCard, hardTotals, softTotals, splits):
    print(cards)
    handTotal = 0
    #handle split
    if cards[0] == cards[1] and len(cards) == 2:
        if cards[0] >= 10 and cards[0] < 14:
            cards[0] = 10
        if dealerCard >= 10 and dealerCard < 14:
            dealerCard = 10   
        splitDecision = (int(splits[dealerCard][int(cards[0])]))
        match splitDecision:
            case 0:
                return 0
            case 1:
                return 3

    #Handle an ace
    elif cards[0] == 14:
        #Max of one hard ace, code it in, if hand exceeds 21, reduce by 10 to soften ace
        handTotal += 10
        if 10 <= cards[1] < 14 and len(cards) == 2:
            return "BlackJack"
        for card in cards:
            #Add a case to resolve soft and hard aces
            if card <= 10:
                handTotal += card
            if card > 10 and card < 14:
                handTotal += 10
            if card == 14:
                handTotal += 1
            if dealerCard > 10 and dealerCard < 14:
                dealerCard = 10
            if dealerCard == 14:
                dealerCard == 11
        if handTotal >= 22:
            handTotal -= 10
            if handTotal > 21:
                return "Bust"
            return int(hardTotals[dealerCard][handTotal])
        if handTotal == 21:
            return 0
        return int(softTotals[dealerCard][handTotal])
    #Default play loop
    else:
        for card in cards:
            #Add a case to resolve soft and hard aces
            if card <= 10:
                handTotal += card
            if card > 10:
                handTotal += 10
        if handTotal > 21:
            return "Bust"
        if handTotal > 17:
            handTotal = 17
        if dealerCard > 10 and dealerCard < 14:
            dealerCard = 10

        #return a enumerated number to denote stand, hit, double, split
        return int(hardTotals[dealerCard][handTotal])
