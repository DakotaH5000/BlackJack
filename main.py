import os
import csv
import pandas as pd
import numpy as np
import random
from gameAction import determinePlayerAction
from gameHelpers import calculateTotals

##A big question while building this is it better to pass integers such as 113 for King or just pass the value of
#K and convert that to a 10.  

#1 is hit or take action, 0 is false or no action, 2 is double down
global hardTotals; pd.DataFrame()
softTotals = pd.DataFrame()
splits = pd.DataFrame()
#import files
hardTotalsCSV = os.path.join('data','hardTotals.csv')
softTotalsCSV = os.path.join('data','softTotals.csv')
splitsCSV = os.path.join('data', 'splits.csv')


deckCount = 4
playerCount = 5
cards = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
letterToSuit = {"S":"Spades", "C":"Clubs", "D":"Diamonds", "H":"Hearts"}
cardValues = [[1,11],10,10,10,10,9,8,7,6,5,4,3,2,1]


#Player status will hold a stood, hit or bust statement for each player
playerStatus=[]

cardsQuantity = {
    14:{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    13:{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    12:{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    11:{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    10:{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    9:{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    8:{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    7:{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    6:{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    5:{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    4:{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    3:{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    2:{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1}
}

#Set the number of cards properly
def buildGameDeck():
    availableCards= []
    for key in cardsQuantity:
        for suit in suits:
                cardsQuantity[key][suit] *= deckCount
                for card in range(0,cardsQuantity[key][suit]):
                    availableCards.append(f'{key}{suit[0]}')
    return availableCards

    


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
def bulidGameHands(gameCards):
    hands = []
    for player in range(0, playerCount + 1):
        hand = random.sample(gameCards, 2)
        hands.append(hand)
        for card in hand:
            gameCards.remove(card)
    return hands


#Key refers to the key:value where cardValue is the value in the relation
#Not very good in time efficency 



def dealerAction(cards, *endOfGame):
    pass


def doubleDown():
    pass

#Take dealer card, total, determine winners and losers, money
def resolveGame(hands):
    results= []
    dealerHand = hands[0]
    dealerTotal = calculateTotals(dealerHand)
    playerHands = hands[1:]
    for hand in playerHands:
        playerTotal = calculateTotals(hand)
        if playerTotal == dealerTotal and playerTotal <= 21:
            results.append("Push")
        elif playerTotal > 21:
            results.append("Bust")
        elif playerTotal == 21 and len(hand) == 2 and dealerTotal != 21:
            results.append("Blackjack")
        elif playerTotal < dealerTotal and playerTotal < 21 and dealerTotal < 22:
            results.append("Lost")
        elif playerTotal < 22 and playerTotal > dealerTotal:
            results.append("Win")
    return results
        
    print(dealerHand)
    print(playerHands)
    pass
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
        hand[i] = int(hand[i][:-1])  # Remove last character (suit)
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

def playGame():
    seenCards = {}
    global splits,softTotals,hardTotals
    splits,softTotals,hardTotals = loadData()
    gameDeck = buildGameDeck()
    gameHands = bulidGameHands(gameDeck)
    print(gameHands)
    hiddenCard = gameHands[0][1]
    #handle player hands as then dealer first card
    for i in range(len(gameHands)-1, 0, -1):
        for card in gameHands[i]:
            if card in seenCards:
                seenCards[card] += 1
            else:
                seenCards[card] = 1
    if gameHands[0][0] in seenCards:
        seenCards[gameHands[0][0]] += 1
    elif gameHands[0][0] not in seenCards:
        seenCards[gameHands[0][0]] = 1
    
    readAbleHand = makeHumanReadable(gameHands)
    dealerHand = trimSuit(gameHands[0])
    playerHands = gameHands[1:]
    print("Readable Hands:")
    dealerValue = dealerHand[0]
    print(f'Dealer shows: {dealerValue}')
    #Stopping iteration at 0 results in dealers hand not being resolved in this set of game actions
    for i in range(len(gameHands)-1, 0, -1):
        hand = trimSuit(gameHands[i])
        sortedHand = sorted(hand, reverse=True)
        print(sortedHand)
        #Method summizes cards, uses tables and current siutaitons to determine game action
        action = determinePlayerAction(sortedHand, dealerValue, hardTotals, softTotals, splits)
        print(action)
        if action == 1:
            while action == 1:
                hand, gameDeck = hit(sortedHand, gameDeck)
                hand[-1] = int(hand[-1][:-1])
                sortedHand = sorted(hand, reverse=True)
                action = determinePlayerAction(sortedHand, dealerValue, hardTotals, softTotals, splits)
                print(sortedHand)
                print(action)
                gameHands[i] = sortedHand
        #Resolve action = 2
        elif action == 3:
            gameHands.remove(hand)
            postSplit = splitHands(sortedHand, gameDeck)
            for i in range(len(postSplit)):
                hand = postSplit[i]
                if hand[1] in seenCards:
                    seenCards[hand[1]] += 1
                else:
                    seenCards[hand[1]] = 1
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
    
    results = resolveGame(gameHands)
    print(results)
    #resolve dealer last card, 
    for i in range(len(gameHands)):
        gameHands[i] = sorted(gameHands[i], reverse=True)
    print(gameHands)
    if gameHands[0][1] in seenCards:
        seenCards[hiddenCard] += 1
    else:
        seenCards[hiddenCard] = 1
    print(seenCards)
        #False parameter is preset, changed to deal with ace H/L

#compare cards, determine split, determine soft or hard total, then determine action, take actinos as neceesary

#generate hands

#compare hands and run simulation

playGame()