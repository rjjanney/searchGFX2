#!/usr/bin/env python

'''
Program to search a text file of directory listings.
Python version = 2.7
*** based on tt070.py from thinking in python ***
'''
import SearchGFX2_classes3_importable as SearchGFX2

import Tkinter as tkt
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open('config.cfg'))

# The location of the text file to search
# FILE_LOCATION = "/Users/206098175/Projects/lists/_FileList.txt"
FILE_LOCATION = config.get('SOURCES', 'FILE_LOCATION')
ROOT = config.get('SOURCES', 'ROOT')

root = tkt.Tk()
myapp = SearchGFX2.MyApp(root)
root.mainloop()
