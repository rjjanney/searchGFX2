#!/usr/bin/env python

'''
Program to search a text file of directory listings.
'''

import sys
import os
import re
import Tkinter, tkFileDialog


# Set up globals and constants ------------------------------------

#root = Tk()
#root.geometry('{}x{}'.format(1000, 400))
#t = Text(root, width=800, height=400)
#t.pack()


# The location of the text file to search
FILE_LOCATION = "/Users/206098175/Projects/searchgfx2/docs/FileList.txt"
# FILE_LOCATION = "/Volumes/GFX2/Graphics/MISC/Lists/FileList_Cct.txt"


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
def apply_patterns(files_list, patterns, search_count):
    search_listed = []
    directory = None
    # for each file in files
    for line in files_list:
        #assign directory line and eliminate it from search
        if line.startswith("/"):
            directory = line.replace(":\n", "")
            continue
        # for each pattern
        for pattern in patterns:
            if pattern.search(line):
                #print search_count, os.path.join(directory, line),
                search_listed.append([search_count, directory, line[:-1]])
                search_count += 1
                
    return search_listed

# For future implementation of search terms that can be booleans or searches of search results
class SearchTerm(object):
    
    def __init__(self, name):
        self.name = name
        self.dirs = []

    def add(directories):
        self.dirs.append(directories)

# unimplemented hyperlinking feature
def openHLink(event):
    start, end = t.tag_prevrange("hlink", t.index("@%s,%s" % (event.x, event.y)))
    print "Going to %s..." % t.get(start, end)

#t.tag_configure("hlink", foreground='blue', underline=1)
#t.tag_bind("hlink", "<Control-Button-1>", openHLink)
def askdirectory():

    """Returns a selected directoryname."""

    root = Tkinter.Tk()
    
    
    dirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
    root.destroy()


    return dirname

# Where the magic happens -----------------------------------------------

try:
    while True:      
        

        search_count = 1

        # Allow for multiple terms: ----------------------------------
        # get search terms
        #search_terms = sys.argv[1:]
        
        #print search_terms
        #sys.exit(1)
        search_terms = raw_input("Search Term: ") # .split(',')
        print search_terms

        if search_terms == "dir":
            dirname = askdirectory()

            if dirname:
            #if len(dirname ) > 0:
                print "You chose %s" % dirname
        else:         
            search_terms = [term.lstrip(" ") for term in search_terms]


            # make search_terms into regex patterns
            outer_patterns = convert_patterns(search_terms)
            # for each pattern:
            with open(FILE_LOCATION, 'r') as file_list:
                search_output = apply_patterns(file_list, outer_patterns, search_count)
                        
                for item in search_output:
                    if item[1] == None:
                        item[1] = ""
                    print item[0], item[1] + "/" + color.BOLD + color.BLUE + item[2] + color.END

            
except KeyboardInterrupt:
    print "\nThanks for playing!"
exit(1)
#root.mainloop()
        
        
# present list as clickable list, with multiple matches in a path
# displaying just the one path
#
# ie directory   filename1
#                filename2
#                filename3
#
# filename should be link to actual file location
# so that clicking on it will open the file
# path should behave the same way


