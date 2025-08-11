from data_helpers import get_expected_value

def calculate_hit(player_value, cards, dealer_value, total_cards):
    expected_value = get_expected_value(total_cards, cards)
    player_expected_value = expected_value + player_value
    dealer_expected_value = expected_value + dealer_value
    print(f' current ev: {player_expected_value} vs {dealer_expected_value}')
    if player_value > dealer_expected_value and player_expected_value > 21:
        return 0
    return "hit"