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

def searcher_submit(search_terms):

    popWindow = Text(root)
    popWindow.rowconfigure(6, weight=1)
    popWindow.grid(rowspan=2, sticky=N+S+E+W)

    scrollbar = Scrollbar(popWindow)
    scrollbar.grid(row=0, sticky=E)

    resultes = Text(popWindow, yscrollcommand = scrollbar.set, padx=30)
    scrollbar.config( command = resultes.yview )    

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
                resultes.insert(END, str(item[0]) + "  " + item[1] + "/" + item[2] + "\n")
    resultes.grid(row=0, column=0, rowspan=2, sticky=NSEW)



class SearcherGUI:
    def __init__(self, top):
        self.top = top
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)
        self.top.title('Search GFX2')
        and_or_state = IntVar()
        anyState = IntVar()
        jpgState = IntVar()
        movState = IntVar()
        tgaState = IntVar()
        wavState = IntVar()
        docState = IntVar()
        c4dState = IntVar()
        psdState = IntVar()
        aeState = IntVar()
        self.and_or_state = and_or_state
        self.anyState = anyState
        self.jpgState = jpgState
        self.movState = movState
        self.tgaState = tgaState
        self.wavState = wavState
        self.docState = docState
        self.c4dState = c4dState
        self.psdState = psdState
        self.aeState = aeState

        self.int_fr = Frame(top)
        self.int_fr.grid(sticky=(N,S,E,W))
        self.int_fr.columnconfigure(0, weight=0)

        self.label = Label(self.int_fr, text="Enter search term(s):")
        self.label.grid()

        self.ent = Entry(self.int_fr)
        self.ent.grid()

        # ---------------------- and / or buttons
        self.frm = Frame(self.int_fr)
        self.frm.grid()

        self.and_button = Radiobutton(self.frm, variable=and_or_state, value=0, text='AND')
        self.and_button.grid(row=0, column=0)

        self.or_button = Radiobutton(self.frm, variable=and_or_state, value=1, text='OR')
        self.or_button.grid(row=0, column=1)

        # ---------------------------------

        self.ent2 = Entry(self.int_fr)
        self.ent2.grid()

        self.btn = Button(self.int_fr, text="Submit", command=(lambda: searcher_submit(self.ent.get())))
        self.btn.grid()

        #----------------------------------- file type buttons group

        self.filetype_frame = LabelFrame(self.int_fr, labelanchor=N, text="File Type", padx=10, pady=10)
        self.filetype_frame.grid(row=0, column=1, rowspan=4)


        self.anyButton = Checkbutton(self.filetype_frame, text="all", variable=anyState, command=self.anyButton_command)
        self.anyButton.grid(row=0, column=0, sticky=W)
        self.anyButton.select()
        self.jpgButton = Checkbutton(self.filetype_frame, text=".jpg", variable=jpgState, command=self.jpgButton_command)
        self.jpgButton.grid(row=0, column=1, sticky=W)
        self.movButton = Checkbutton(self.filetype_frame, text=".mov", variable=movState, command=self.movButton_command)
        self.movButton.grid(row=0, column=2, sticky=W)
        self.tgaButton = Checkbutton(self.filetype_frame, text=".tga", variable=tgaState, command=self.tgaButton_command)
        self.tgaButton.grid(row=1, column=0, sticky=W)
        self.wavButton = Checkbutton(self.filetype_frame, text=".wav", variable=wavState, command=self.wavButton_command)
        self.wavButton.grid(row=1, column=1, sticky=W)
        self.docButton = Checkbutton(self.filetype_frame, text=".doc", variable=docState, command=self.docButton_command)
        self.docButton.grid(row=1, column=2, sticky=W)
        self.c4dButton = Checkbutton(self.filetype_frame, text=".c4d", variable=c4dState, command=self.c4dButton_command)
        self.c4dButton.grid(row=2, column=0, sticky=W)
        self.psdButton = Checkbutton(self.filetype_frame, text=".psd", variable=psdState, command=self.psdButton_command)
        self.psdButton.grid(row=2, column=1, sticky=W)
        self.aeButton = Checkbutton(self.filetype_frame, text=".ae", variable=aeState, command=self.aeButton_command)
        self.aeButton.grid(row=2, column=2, sticky=W)

        #-----------------------------------

        self.dirBtn = Button(self.int_fr, text="Choose Directory", command=self.dirBtn_command)
        self.dirBtn.grid(column=1, row=4)

    def checkButtonsStates(self):
        if (   self.jpgState.get() 
            or self.movState.get() 
            or self.tgaState.get() 
            or self.wavState.get() 
            or self.docState.get() 
            or self.c4dState.get() 
            or self.psdState.get() 
            or self.aeState.get()):
            pass
        else:
            self.anyButton.toggle() 

    def anyButton_command(self):
        self.jpgButton.deselect()
        self.movButton.deselect()
        self.tgaButton.deselect()
        self.wavButton.deselect()
        self.docButton.deselect()
        self.c4dButton.deselect()
        self.psdButton.deselect()
        self.aeButton.deselect()
        
    def jpgButton_command(self):
        if self.jpgState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def movButton_command(self):
        if self.movState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def tgaButton_command(self):
        if self.tgaState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()
    def wavButton_command(self):
        if self.wavState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def docButton_command(self):
        if self.docState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def c4dButton_command(self):
        if self.c4dState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def psdButton_command(self):
        if self.psdState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def aeButton_command(self):
        if self.aeState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def dirBtn_command(self):
        popWindow = Toplevel()
        scrollbar = Scrollbar(popWindow)
        scrollbar.pack( side = RIGHT, fill=Y )

        resultes = Text(popWindow, yscrollcommand = scrollbar.set, wrap=WORD)
        scrollbar.config( command = resultes.yview )

        for line in range(100):
           resultes.insert(END, "This is line number " + str(line) + "\n")

        resultes.pack( side = LEFT, fill = BOTH )
        




        resultes.insert(0.0, "I'm a little teapot, short and stout.\n")

    # Where the magic happens -----------------------------------------------

root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


search_GUI = SearcherGUI(root)

root.mainloop()