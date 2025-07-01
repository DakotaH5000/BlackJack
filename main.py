import os
import csv
import pandas as pd
import numpy as np
import random

##A big question while building this is it better to pass integers such as 113 for King or just pass the value of
#K and convert that to a 10.  

#1 is hit or take action, 0 is false or no action, 2 is double down
hardTotals = pd.DataFrame()
softTotals = pd.DataFrame()
splits = pd.DataFrame()
#import files
hardTotalsCSV = os.path.join('data','hardTotals.csv')
softTotalsCSV = os.path.join('data','softTotals.csv')
splitsCSV = os.path.join('data', 'splits.csv')

deckCount = 2
playerCount = 3
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

        hardTotals = pd.DataFrame(data, index=[17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],columns=header)

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



def determinePlayerAction(cards, dealerCard,  *recursive):
    handTotal = 0
    for card in cards:
        #Add a case to resolve soft and hard aces
        if card <= 10:
            handTotal += card
        if card > 10:
            handTotal += 10
    if handTotal > 17:
        handTotal = 17
    if dealerCard > 10 and dealerCard < 14:
        dealerCard = 10

    #return a enumerated number to denote stand, hit, double, split
    return hardTotals[dealerCard][handTotal]

def dealerAction(cards, *endOfGame):
    pass

def addCard():
    pass
        
#print("Hard totals:")
#print(hardTotals)
#print("Soft Totals:")
#print(softTotals)
#print("Splits:")
#print(splits)
#print("End file")
#stores with headers and insert card total in [x][0] of every row

#print(cardsQuantity)

def hit(cardsInDeck:list, currentCards):
    pass

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
    print(returnHands)
    return returnHands

def playGame():
    global splits,softTotals,hardTotals
    splits,softTotals,hardTotals = loadData()
    gameDeck = buildGameDeck()
    gameHands = bulidGameHands(gameDeck)
    print(gameDeck)
    print(gameHands)
    readAbleHand = makeHumanReadable(gameHands)
    dealerHand = trimSuit(gameHands[0])
    playerHands = gameHands[1:]
    print("Start Game!")
    print("Readable Hands:")
    dealerValue = dealerHand[0]
    print(f'Dealer shows: {dealerValue}')
    #Stopping iteration at 0 results in dealers hand not being resolved in this set of game actions
    for i in range(len(gameHands)-1, 0, -1):
        hand = trimSuit(gameHands[i])
        sortedHand = sorted(hand, reverse=True)
        print(sortedHand)
        #Method summizes cards, uses tables and current siutaitons to determine game action
        action = determinePlayerAction(sortedHand, dealerValue)
        
        #Method to resolve game action

        #False parameter is preset, changed to deal with ace H/L

#compare cards, determine split, determine soft or hard total, then determine action, take actinos as neceesary

#generate hands

#compare hands and run simulation

playGame()