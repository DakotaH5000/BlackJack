import os
import csv
import pandas as pd

#1 is hit or take action, 0 is false or no action, 2 is double down
hardTotals = pd.DataFrame()
softTotals = pd.DataFrame()
splits = pd.DataFrame()
#import files
hardTotalsCSV = os.path.join('data','hardTotals.csv')
softTotalsCSV = os.path.join('data','softTotals.csv')
splitsCSV = os.path.join('data', 'splits.csv')

deckCount = 1
cards = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
suits = ["Spades", "Clubs", "Diamonds", "Hearts"]

cardsQuantity = {
    "A":{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    "K":{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    "Q":{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    "J":{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    "10":{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    "9":{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    "8":{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    "7":{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    "6":{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    "5":{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    "4":{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    "3":{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1},
    "2":{"Spades":1, "Clubs":1, "Diamonds": 1, "Hearts":1}
}

#Set the number of cards properly
for key in cardsQuantity:
    for suit in suits:
        if suit == "Spades":
            cardsQuantity[key][suit] *= 3
    print(cardsQuantity[key])
    


#Populate dataframes with csv data
with open(splitsCSV, 'r') as file:
    csvreader = csv.reader(file)
    rows = list(csvreader)
    header = rows[0]
    data = rows[1:]
    splits = pd.DataFrame(data, index=["A",10,9,8,7,6,5,4,3,2],columns=header)
with open(softTotalsCSV, 'r') as file:
    csvreader = csv.reader(file)
    rows = list(csvreader)
    header = rows[0]
    data = rows[1:]
    softTotals = pd.DataFrame(data, index=[20,19,18,17,16,15,14,13],columns=header)
with open(hardTotalsCSV, 'r') as file:
    csvreader = csv.reader(file)
    rows = list(csvreader)
    header = rows[0]
    data = rows[1:]
    hardTotals = pd.DataFrame(data, index=["17","16","15","14","13","12","11","10","9","8"],columns=header)


#print("Hard totals:")
#print(hardTotals)
#print("Soft Totals:")
#print(softTotals)
#print("Splits:")
#print(splits)
#print("End file")
#stores with headers and insert card total in [x][0] of every row

#print(cardsQuantity)


#compare cards, determine split, determine soft or hard total, then determine action, take actinos as neceesary

#generate hands

#compare hands and run simulation