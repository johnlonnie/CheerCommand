import csv

#game
currentGameConfig = "pubg.csv"

#idle time for commands that require a time out
idleTime = 10

#channel point identifiers - when a user redeems channel points, the channel point will have an identifier (e.g. "b3df3074-eb94-4f44-811a-1815835edfdd")
channelPoint1 = ""

#WASD - hard-coded bit costs for Wacky Wasd function
subWASD = 333
WASD = 666

#import commands
cost = []
discount = []
description = []
kind = []
action = []
actionDetail = []
duration = []
action2 = []

row_count = 0

with open(currentGameConfig) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        cost.append(row[0])
        discount.append(row[1])
        description.append(row[2])
        kind.append(row[3])
        action.append(row[4])
        actionDetail.append(row[5])
        duration.append(row[6])
        action2.append(row[7])
with open(currentGameConfig) as f:
    row_count = sum(1 for line in f)	