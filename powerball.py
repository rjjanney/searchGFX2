#!/usr/bin/python


import csv
with open('powerball.csv', 'rb') as f:
    reader = csv.reader(f)
    thingy = []
    for row in reader:
        thingy.append(row)
    pickNumber = 1
    atLeastOne = []
    moreThanOne = []
    tempReader = []
    searchTermList = []
    while pickNumber < 6:
        print("Please enter the next number:")
        searchTerm = raw_input("> ")
        searchTermList.append(searchTerm)
        for row in thingy:
            print row
            for idx in range(0,5):
                if searchTerm in row[idx]:
                    tempReader.append(row)

        if len(tempReader) > 0:
            for row in tempReader:
                if row in atLeastOne:
                    moreThanOne.append(row)

            atLeastOne.extend(tempReader)
            tempReader = []

        print "You matched %d :" % pickNumber
        for element in range(len(atLeastOne)):
            print atLeastOne[element]

        pickNumber += 1

    print "\n------------------------------"
    searchTermList.sort()
    print searchTermList
    print ".............................."
    for element in range(len(moreThanOne)):
            print moreThanOne[element]



