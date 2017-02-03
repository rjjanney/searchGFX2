#!/usr/bin/python


import csv
with open('powerball.csv', 'rb') as f:
    reader = csv.reader(f)
    thingy = []
    print reader
    for row in reader:
        thingy.append(row)
    print thingy    

