import os
import csv
import pandas as pd
import numpy as np
import random
from data.datatypes import cardsQuantity,cards,suits,letterToSuit,cardValues
from gameAction import determinePlayerAction
from gameHelpers import calculate_totals, build_game_deck
from calculateCurrentOdds import estimate_decks_confidence
from calculatedOddsActions import determine_action_odds

##A big question while building this is it better to pass integers such as 113 for King or just pass the value of
#K and convert that to a 10.  

#1 is hit or take action, 0 is false or no action, 2 is double down
global hardTotals; pd.DataFrame()
softTotals = pd.DataFrame()
splits = pd.DataFrame()
seen_cards= {}
#import files
hardTotalsCSV = os.path.join('data','hardTotals.csv')
softTotalsCSV = os.path.join('data','softTotals.csv')
splitsCSV = os.path.join('data', 'splits.csv')


deckCount = random.randint(1,10)
playerCount = 5



#Player status will hold a stood, hit or bust statement for each player
playerStatus=[]




    


#Populate dataframes with csv data
def loadData():
    with open(splitsCSV, 'r') as file:
        csvreader = csv.reader(file)
        rows = list(csvreader)
        header = list(map(int, rows[0]))
        data = rows[1:]
        splits = pd.DataFrame(data, index=[14,10,9,8,7,6,5,4,3,2],columns=header)
    with open(softTotalsCSV, 'r') as file:
        csvreader = csv.reader(file)
        rows = list(csvreader)
        header = list(map(int, rows[0]))
        data = rows[1:]
        softTotals = pd.DataFrame(data, index=[20,19,18,17,16,15,14,13],columns=header)
    with open(hardTotalsCSV, 'r') as file:
        csvreader = csv.reader(file)
        rows = list(csvreader)
        header = list(map(int, rows[0]))
        data = rows[1:]

        hardTotals = pd.DataFrame(data, index=[21,20,19,18,17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],columns=header)

        return splits,softTotals,hardTotals



#hands generates the numerical representation of the game state, readable hand provides a user readable interface to better understand game states and actions
#Generates card without suit
def build_game_hands(gameCards):
    hands = []
    for player in range(0, playerCount + 1):
        hand = random.sample(gameCards, 2)
        hands.append(hand)
        for card in hand:
            gameCards.remove(card)
    return hands


#Key refers to the key:value where cardValue is the value in the relation
#Not very good in time efficency 


#Logic does not work with multiple aces, need fix
def dealerAction(cards, deck):
    print(cards)
    handTotal = 0
    while handTotal < 17:
        handTotal = calculate_totals(cards)
        if handTotal < 17:
            cards, deck = hit(cards, deck)
            print(cards[-1])
            cards[-1] = int(cards[-1][:-1])

    return cards, handTotal



def doubleDown():
    pass

#Take dealer card, total, determine winners and losers, money
def resolveGame(dealer, players):
    results= []
    dealerTotal = dealer
    print(dealer, players)
    playerHands = players
    for hand in playerHands:
        playerTotal = calculate_totals(hand)
        if playerTotal == dealerTotal and playerTotal <= 21:
            results.append(["Push", hand])
        elif playerTotal >= 22:
            results.append(["Bust", hand])
        elif playerTotal == 21 and len(hand) == 2 and dealerTotal != 21:
            results.append(["Blackjack", hand])
        elif playerTotal < dealerTotal and playerTotal < 21 and dealerTotal < 22:
            results.append(["Lost", hand])
        elif (playerTotal < 22 and playerTotal > dealerTotal) or (playerTotal < 22 and dealerTotal > 21):
            results.append(["Win", hand])
    return results
        
#take gameHands[X], create gameHands[Y], gameHands[Z] with X 0 and 1 being 0 in both hands, add new cards to 
#seen cards resolve game hand 1 in loop, game hand 2 should finish while checking the list
def splitHands(hands, gameCards):
        hand1 = [hands[0]]
        hand2 = [hands[1]]
        hand1Card = random.sample(gameCards, 1)
        hand1.append(hand1Card[0])
        gameCards.remove(hand1Card[0])
        hand2Card = random.sample(gameCards, 1)
        hand2.append(hand2Card[0])
        gameCards.remove(hand2Card[0])
        return [hand1, hand2]

def hit(hand:list, cardsInDeck:list):
    hitCard = random.sample(cardsInDeck, 1)[0]
    hand.append(hitCard)
    cardsInDeck.remove(hitCard)

    return hand, cardsInDeck

def trimSuit(hand):
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

    

def makeHumanReadable(hands):
    returnHands = []
    for hand in hands:
        cardValueNoSuit = []
        for card in hand:
            if card[0] == '1':
                if card[1] == '0':
                    cardsQuantity[int(card[:2])][letterToSuit[card[2]]] -= 1
                    cardValueNoSuit.append(f'{card[0]}{card[1]}')
                elif card[1] == '1':
                    cardsQuantity[int(card[:2])][letterToSuit[card[2]]] -= 1
                    cardValueNoSuit.append(f'{cards[3]}')
                elif card[1] == '2':
                    cardsQuantity[int(card[:2])][letterToSuit[card[2]]] -= 1
                    cardValueNoSuit.append(f'{cards[2]}')
                elif card[1] == '3':
                    cardsQuantity[int(card[:2])][letterToSuit[card[2]]] -= 1
                    cardValueNoSuit.append(f'{cards[1]}')
                elif card[1] == '4':
                    cardsQuantity[int(card[:2])][letterToSuit[card[2]]] -= 1
                    cardValueNoSuit.append(f'{cards[0]}')
            else:
                cardsQuantity[int(card[0])][letterToSuit[card[1]]] -= 1
                cardValueNoSuit.append(card[0])
        returnHands.append(cardValueNoSuit)
    return returnHands

def gameSetup(deckCount):
    global splits,softTotals,hardTotals
    splits,softTotals,hardTotals = loadData()
    gameDeck = build_game_deck(deckCount)

    return splits,softTotals,hardTotals, gameDeck

def playGame(games):
    currentGame = 0
    while currentGame < games :
        global splits,softTotals,hardTotals, gameDeck
        if currentGame == 0:
            splits,softTotals,hardTotals, gameDeck = gameSetup(deckCount)
        gameHands = build_game_hands(gameDeck)

        #print(gameHands)

        hiddenCard = gameHands[0][1]

        #handle player hands as then dealer first card
        for i in range(len(gameHands)-1, 0, -1):
            for card in gameHands[i]:
                if card in seen_cards:
                    seen_cards[card] += 1
                else:
                    seen_cards[card] = 1


        #Include dealer face-up card in observations
        if gameHands[0][0] in seen_cards:
            seen_cards[gameHands[0][0]] += 1
        elif gameHands[0][0] not in seen_cards:
            seen_cards[gameHands[0][0]] = 1
        
        readAbleHand = makeHumanReadable(gameHands)
        dealerHand = trimSuit(gameHands[0])
        playerHands = gameHands[1:]
        dealerValue = dealerHand[0]
        #print(f'Dealer shows: {dealerValue}')
        #Stopping iteration at 0 results in dealers hand not being resolved in this set of game actions
        for i in range(len(playerHands)):
            hand = trimSuit(playerHands[i])
            sortedHand = sorted(hand, reverse=True)

            probabilites = estimate_decks_confidence(seen_cards,10)["probabilities"]
            computedAction = determine_action_odds(probabilites, seen_cards, sortedHand, dealerValue)


            action = determinePlayerAction(sortedHand, dealerValue, hardTotals, softTotals, splits)
            if action == 1:
                while action == 1:
                    hand, gameDeck = hit(sortedHand, gameDeck)
                    if hand[-1] in seen_cards:
                        seen_cards[hand[-1]] += 1
                    else:
                        seen_cards[hand[-1]] = 1
                    hand = trimSuit(hand)
                    sortedHand = sorted(hand, reverse=True)
                    action = determinePlayerAction(sortedHand, dealerValue, hardTotals, softTotals, splits)
                    gameHands[i] = sortedHand
            #Resolve action = 2
            elif action == 3:
                gameHands.remove(hand)
                postSplit = splitHands(sortedHand, gameDeck)
                for i in range(len(postSplit)):
                    hand = postSplit[i]
                    if hand[1] in seen_cards:
                        seen_cards[hand[1]] += 1
                    else:
                        seen_cards[hand[1]] = 1
                    hand[1] = int(hand[1][:-1])
                    sortedHand = sorted(hand, reverse=True)
                    action = determinePlayerAction(sortedHand, dealerValue, hardTotals, softTotals, splits)
                    if action == 1:
                        while action == 1:
                            hand, gameDeck = hit(sortedHand, gameDeck)
                            hand[-1] = int(hand[-1][:-1])
                            sortedHand = sorted(hand, reverse=True)
                            action = determinePlayerAction(sortedHand, dealerValue, hardTotals, softTotals, splits)
                    gameHands.append(hand)
        dealerHand, dealerTotal = dealerAction(dealerHand, gameDeck)
        dealerTotal = int(dealerTotal)
        results = resolveGame(dealerTotal, gameHands[1:])

        #resolve dealer last card, 
        for i in range(len(gameHands)):
            gameHands[i] = sorted(gameHands[i], reverse=True)
        #print(estimate_decks_confidence(seen_cards, 10))

        #print(probabilites)
        #print(deckCount)
        if gameHands[0][1] in seen_cards:
            seen_cards[hiddenCard] += 1
        else:
            seen_cards[hiddenCard] = 1
            #False parameter is preset, changed to deal with ace H/L
        currentGame+=1
    
    quit

    #compare cards, determine split, determine soft or hard total, then determine action, take actinos as neceesary

    #generate hands

    #compare hands and run simulation

playGame(3)