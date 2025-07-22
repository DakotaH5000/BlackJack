from gameHelpers import buildGameDeck
#Using the probabilites item of the distriubtion, create a voting system where each game state is calculated
#each deckCount votes with weighting on their respective choice

def determine_action_odds(probs):
    for i in range(len(probs)):
        #take prob, build a deck
        print(i)
        buildGameDeck(i+1)
