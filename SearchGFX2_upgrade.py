#!/usr/bin/env python

'''
Program to search a text file of directory listings.
'''

import sys
import os
import re
from Tkinter import *
from tkMessageBox import showinfo

# The location of the text file to search
# FILE_LOCATION = "/Users/206098175/Projects/searchgfx2/docs/FileList.txt"
FILE_LOCATION = "/Volumes/GFX2/Graphics/MISC/Lists/FileList_Cct.txt"

# Class and function definitions -----------------------------------

# Custom colors for indicating files vs folders vs disks
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# This converts the search strings to regex patterns
def convert_patterns(patterns):
    results = []
    # for each pattern
    #for pattern in patterns:
    #    print pattern
        #make a regex with it
    results = [re.compile(p, re.IGNORECASE) for p in patterns]
    return results

# Finds and compiles the results of the regex search.
def apply_pattern(files_list, pattern, search_count):
    search_listed = []
    directory = None
    # for each file in files
    for line in files_list:
        #assign directory line and eliminate it from search
        if line.startswith("/"):
            directory = line.replace(":\n", "")
            continue
        # for each pattern
        if pattern.search(line):
            #print search_count, os.path.join(directory, line),
            search_listed.append([search_count, directory, line[:-1]])
            search_count += 1
            
    return search_listed

def checkButtonsStates():
    if not jpgButton.get() and movButton and tgaButton and wavButton and docButton and c4dButton and psdButton and aeButton:
        anyButton.select() 

def anyButton_command():
    jpgButton.deselect()
    movButton.deselect()
    tgaButton.deselect()
    wavButton.deselect()
    docButton.deselect()
    c4dButton.deselect()
    psdButton.deselect()
    aeButton.deselect()
    
def jpgButton_command():
    if jpegButton.get():
        anyButton.deselect()
    else:
        checkButtonsStates()

def movButton_command():
    anyButton.deselect()

def tgaButton_command():
    anyButton.deselect()

def wavButton_command():
    anyButton.deselect()

def docButton_command():
    anyButton.deselect()

def c4dButton_command():
    anyButton.deselect()

def psdButton_command():
    anyButton.deselect()

def aeButton_command():
    anyButton.deselect()

# Where the magic happens -----------------------------------------------

def searcher_submit(search_terms):
        search_count = 1

        search_terms = search_terms.split(',')
        search_terms = [term.lstrip(" ") for term in search_terms]


        # make search_terms into regex patterns
        outer_patterns = convert_patterns(search_terms)
        # for each pattern:
        with open(FILE_LOCATION, 'r') as file_list:
            for out_pattern in outer_patterns:
                search_output = apply_pattern(file_list, out_pattern, search_count)
                    
                for item in search_output:
                    if item[1] == None:
                        item[1] = ""
                    print item[0], item[1] + "/" + color.BOLD + color.BLUE + item[2] + color.END

#--------------The Application Window --------------

top = Tk()
top.title('Search GFX2')
top.grid_columnconfigure(0, pad=30)
top.grid_columnconfigure(1, pad=30)

and_or_state = IntVar()

# anyButton = IntVar()
# jpgButton = IntVar()
# movButton = IntVar()
# tgaButton = IntVar()
# wavButton = IntVar()
# docButton = IntVar()
# c4dButton = IntVar()
# psdButton = IntVar()
# aeButton = IntVar()

Label(top, text="Enter search term(s):").grid()

ent = Entry(top)
ent.grid()

# ----------------------
frm = Frame(top)
frm.grid()

and_button = Radiobutton(frm, variable=and_or_state, value=0, text='AND')
and_button.grid(row=0, column=0)

or_button = Radiobutton(frm, variable=and_or_state, value=1, text='OR')
or_button.grid(row=0, column=1)

# ---------------------------------

ent2 = Entry(top)
ent2.grid()

btn = Button(top, text="Submit", command=(lambda: searcher_submit(ent.get())))
btn.grid()

filetype_frame = LabelFrame(top, labelanchor=N, text="File Type", padx=10, pady=10)
filetype_frame.grid(row=0, column=1, rowspan=3)


anyButton = Checkbutton(filetype_frame, text="all", command=anyButton_command)
anyButton.grid(row=0, column=0, sticky=W)
jpgButton = Checkbutton(filetype_frame, text=".jpg", command=jpgButton_command)
jpgButton.grid(row=0, column=1, sticky=W)
movButton = Checkbutton(filetype_frame, text=".mov")
movButton.grid(row=0, column=2, sticky=W)
tgaButton = Checkbutton(filetype_frame, text=".tga")
tgaButton.grid(row=1, column=0, sticky=W)
wavButton = Checkbutton(filetype_frame, text=".wav")
wavButton.grid(row=1, column=1, sticky=W)
docButton = Checkbutton(filetype_frame, text=".doc")
docButton.grid(row=1, column=2, sticky=W)
c4dButton = Checkbutton(filetype_frame, text=".c4d")
c4dButton.grid(row=2, column=0, sticky=W)
psdButton = Checkbutton(filetype_frame, text=".psd")
psdButton.grid(row=2, column=1, sticky=W)
aeButton = Checkbutton(filetype_frame, text=".ae")
aeButton.grid(row=2, column=2, sticky=W)

top.mainloop()




