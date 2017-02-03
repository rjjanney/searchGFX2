#!/usr/bin/env python

'''
Program to search a text file of directory listings.

*** based on tt070.py from thinking in python ***
'''

import sys
import os
import re
from Tkinter import *
import tkFileDialog
import subprocess

# CONSTANTS --------------------------------------------------------

# The location of the text file to search
FILE_LOCATION = "/Users/206098175/Projects/lists/_FileList.txt"
# FILE_LOCATION = "/Volumes/GFX2/Graphics/MISC/Lists/FileList_Cct.txt"
ROOT = "/Volumes/GFX2/_Graphics"

# Class and function definitions -----------------------------------

# This converts the search strings to regex patterns
def convert_patterns(patterns):
    results = []
    # for each pattern
    #for pattern in patterns:
    #    print pattern
        #make a regex with it
    results = [re.compile(p + ".*(" + myapp.endings + ")$", re.IGNORECASE) for p in patterns]
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
            search_listed.append([search_count, directory, line[:-1]])
            search_count += 1
    # print search_listed        
    return search_listed

def searcher_submit(search_terms):

    # ENABLES EDITING IN RESULT WINDOW
    myapp.results_window.config(state=NORMAL)
    myapp.results_window.tag_config("file", foreground="blue")
    search_count = 1

    search_terms = search_terms.split(',')
    search_terms = [term.lstrip(" ") for term in search_terms]

    # make search_terms into regex patterns
    outer_patterns = convert_patterns(search_terms)
    # for each pattern:
    with open(FILE_LOCATION, 'r') as file_list:
        for out_pattern in outer_patterns:
            search_output = apply_pattern(file_list, out_pattern, search_count)
            item = [0,0,0]    
            for item in search_output:
                # for filename highlighting, holds last line index, eventually
                temp_index = 0
                if item[1] == None:
                    item[1] = ROOT
                if myapp.search_root not in item[1]:
                    continue
                myapp.results_window.insert(END, item[1] + "/" + item[2] + "\n")
                filename_end =  str(myapp.line_index) + "." + str(len(item[1]) + len(item[2]) + 1)
                filename_begin = str(myapp.line_index) + "." + str(len(item[1]) + 1)
                myapp.results_window.tag_add("file", filename_begin, filename_end)
                myapp.line_index += 1                
       
        myapp.filecount.config(text="Files Found: %d" %  (myapp.line_index - 1), fg="black")
        myapp.cleared = False
        
        # DISABLES EDITING IN RESULT WINDOW
        myapp.results_window.config(state=DISABLED)


class MyApp:
    def __init__(self, parent):
        self.myParent = parent
        parent.bind('<Return>', self.return_funct)
        parent.title("Search GFX2")

        #______ INITIALIZE VARIABLES _________
        self.and_or_state = IntVar()
        self.anyState = IntVar()
        self.jpgState = IntVar()
        self.movState = IntVar()
        self.tgaState = IntVar()
        self.wavState = IntVar()
        self.docState = IntVar()
        self.c4dState = IntVar()
        self.psdState = IntVar()
        self.aeState = IntVar()
        self.search_root = StringVar()
        self.search_root = ROOT
        self.line_index = 1
        self.endings = StringVar()
        self.endings = ""
        self.endings_list = []
        self.sep = "|"



        #________ THE WIDGETS __________________
        self.frame1 = Frame(parent)
        self.frame2 = Frame(parent)
        self.frame2a = Frame(parent)
        self.frame3 = Frame(parent)
        self.frame4 = Frame(parent, padx=10, pady=6)
        self.frame5 = Frame(parent, padx=10, pady=6)
        self.tl_frm = Frame(self.frame1)
        self.tr_frm = Frame(self.frame1)


        self.label = Label(self.tl_frm, text="Enter search term(s):")
        self.ent = Entry(self.tl_frm)
        self.ao_frm = Frame(self.tr_frm)
        self.and_button = Radiobutton(self.ao_frm, variable=self.and_or_state, value=0, text='AND')
        self.or_button = Radiobutton(self.ao_frm, variable=self.and_or_state, value=1, text='OR')
        self.not_button = Radiobutton(self.ao_frm, variable=self.and_or_state, value=2, text="NOT")
        self.ent2 = Entry(self.tr_frm)
        
        self.btn = Button(self.tr_frm, text="Search",  
            command=self.search_funct)

        #________ 9 Filetype Buttons ____________
        self.filetype_frame = LabelFrame(self.frame2)
        self.anyButton = Checkbutton(self.filetype_frame, text="all", variable=self.anyState, command=self.anyButton_command, justify=LEFT, padx=5)
        self.anyButton.select()
        self.jpgButton = Checkbutton(self.filetype_frame, text=".jpg", variable=self.jpgState, command=self.jpgButton_command, justify=LEFT, padx=5)
        self.movButton = Checkbutton(self.filetype_frame, text=".mov", variable=self.movState, command=self.movButton_command, justify=LEFT, padx=5)
        self.tgaButton = Checkbutton(self.filetype_frame, text=".tga", variable=self.tgaState, command=self.tgaButton_command, justify=LEFT, padx=5)
        self.wavButton = Checkbutton(self.filetype_frame, text=".wav", variable=self.wavState, command=self.wavButton_command, justify=LEFT, padx=5)
        self.docButton = Checkbutton(self.filetype_frame, text=".doc", variable=self.docState, command=self.docButton_command, justify=LEFT, padx=5)
        self.c4dButton = Checkbutton(self.filetype_frame, text=".c4d", variable=self.c4dState, command=self.c4dButton_command, justify=LEFT, padx=5)
        self.psdButton = Checkbutton(self.filetype_frame, text=".psd", variable=self.psdState, command=self.psdButton_command, justify=LEFT, padx=5)
        self.aeButton = Checkbutton(self.filetype_frame, text=".ae", variable=self.aeState, command=self.aeButton_command, justify=LEFT, padx=5)
        
        self.dirBtn = Button(self.frame2a, text="Choose Directory", command=self.dirBtn_command)
        self.dirLbl = Label(self.frame2a, text="Searching in: " + self.search_root)
        
        #__________ RESULTS Window ________________
        self.scrollbar = Scrollbar(self.frame4)
        self.results_window = Text(self.frame4, relief=GROOVE, bd=1, yscrollcommand=self.scrollbar.set)
        self.filecount = Label(self.frame5, text="Files Found: 0", fg="black")
        self.clear_button = Button(self.frame5, text="Clear Result Box", command=self.clear_button_command)

        #___________ LAYOUT _________________
        
        self.frame5.pack(side=BOTTOM, fill=X)
        self.frame4.pack(side=BOTTOM, expand=YES, fill=BOTH)
        self.frame2a.pack(side=BOTTOM, expand=YES, fill=BOTH)
        self.frame1.pack(side=LEFT, expand=YES, fill=BOTH, padx=10)
        self.frame2.pack(side=LEFT, expand=YES, fill=BOTH)
        self.frame3.pack(side=LEFT, expand=YES, fill=BOTH)
        
        self.tl_frm.pack(side=LEFT)
        self.label.pack(side=LEFT)
        self.ent.pack(side=LEFT)
        self.tr_frm.pack(side=RIGHT)
        self.ao_frm.configure(padx=4)
        self.ao_frm.pack(side=LEFT, expand=YES, fill=BOTH)
        self.and_button.pack(side=LEFT)
        self.or_button.pack(side=LEFT)
        self.not_button.pack(side=RIGHT)
        self.ent2.pack(side=LEFT)

        self.filetype_frame.pack(side=LEFT, expand=YES, padx=10)
        self.anyButton.pack(side=LEFT)
        self.jpgButton.pack(side=LEFT)
        self.movButton.pack(side=LEFT)
        self.tgaButton.pack(side=LEFT)
        self.wavButton.pack(side=LEFT)
        self.docButton.pack(side=LEFT)
        self.c4dButton.pack(side=LEFT)
        self.psdButton.pack(side=LEFT)
        self.aeButton.pack(side=LEFT)
        self.dirLbl.pack(side=LEFT, fill=X, padx=10)
        self.dirBtn.pack(side=LEFT, expand=NO, padx=10)
        
        self.btn.pack(side=LEFT, expand=YES, fill=X)

        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.results_window.pack(side=TOP, expand=YES, fill=BOTH)
        self.results_window.bind('<Button-1>', self.select_line)
        
        self.filecount.pack(side=LEFT, fill=X)
        self.clear_button.pack(side=RIGHT)
        self.scrollbar.config(command=self.results_window.yview)

        
        self.end_buttons = {"jpg": (self.jpgState, self.jpgButton, "jpg|jpeg"), 
                            "mov": (self.movState, self.movButton, "mov|mxf"),
                            "tga": (self.tgaState, self.tgaButton, "tga"),
                            "wav": (self.wavState, self.wavButton, "wav|aif|aiff|mp3|ogg"),
                            "doc": (self.docState, self.docButton, "doc|docx|txt|rtf|pdf"),
                            "c4d": (self.c4dState, self.c4dButton, "c4d|obj|mb|mel"),
                            "psd": (self.psdState, self.psdButton, "psd"),
                            "ae":  (self.aeState,  self.aeButton,  "ae|aep")
                            }

    #_________ BINDINGS __________________________
    
    def return_funct(self, event=None):
        self.search_funct()

    def search_funct(self, event=None):
        # SEARCHING NOTIFICATION
        self.filecount.config(text="SEARCHING...", fg="red")
        self.filecount.update_idletasks()

        for val in self.end_buttons.viewvalues():
            if val[0].get():
                self.endings_list.append(val[2])
        self.endings = self.sep.join(self.endings_list)
        # for testing
        # print self.endings
        searcher_submit(self.ent.get())
        self.endings_list = []

    def select_line(self, event):
        # get index of text under mouse position in text widget
        index = self.results_window.index("@%s,%s" % (event.x, event.y))
        # select that whole line and assign it to file_loc
        file_loc = self.results_window.get("%s linestart" % index, "%s lineend" % index)
        # pop open finder window containing file, if line contains any info
        if file_loc != "":
            subprocess.call(["open", "-R", file_loc])

    def checkButtonsStates(self):
        on_off = []
        for val in self.end_buttons.viewvalues():
            on_off.append(val[0].get())
        if 1 in on_off:
            pass
        else:
            self.anyButton.toggle() 
            self.endings = ""

    def anyButton_command(self):
        for val in self.end_buttons.viewvalues():
            val[1].deselect()
        self.anyButton.select()
        self.endings = ""
        
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
        """
        Pop up file directory choose dialog box
        Passes chosen directory into the object
        """
        self.search_root = tkFileDialog.askdirectory(initialdir=ROOT)
        self.dirLbl.config(text="Searching in: " + self.search_root)

        
    def clear_button_command(self):
        # ENABLES EDITING IN RESULT WINDOW
        self.results_window.config(state=NORMAL)
        self.results_window.delete(1.0, END)
        self.line_index = 1
        # DISABLES EDITING IN RESULT WINDOW
        self.results_window.config(state=DISABLED)
        self.filecount.config(text="Files Found: 0")

root = Tk()
myapp = MyApp(root)
root.mainloop()