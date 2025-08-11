def get_expected_value(num_cards, card_counts):
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