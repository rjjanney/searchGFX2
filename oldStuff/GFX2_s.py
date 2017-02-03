#!/usr/bin/python

from sys import exit

try:
    while True:
        myList = open('/Volumes/GFX2/Graphics/MISC/Lists/FileList_Cct.txt', 'r')
        print("Please enter your search term (CTL-C to quit):")
        searchTerm = raw_input("> ")
        
        # search (and print for now)
        
        checkDir = False
        count=0
        big2DList=[]
        tmpList=[]
        
        
        
        for line in myList:
            if line.startswith("/"):
                
                # remove ":" from end of directory listing
                dirTmp = line.replace(":", "")
               
                checkDir = True
                #print(dirTmp)
            elif line.lower().find(searchTerm.lower()) > -1 :
                if checkDir:
                    big2DList.append(tmpList)
                    tmpList=[]
                    tmpList.append(dirTmp)
                    checkDir = False
                count +=1
                # without count:
                # tmpList.append(line)
                # to add count:
                tmpList.append(str(count)+" " + line)
                
            else:
                pass
        myList.close()
        
        # when search term found:
            # Save filename, path, date, to list. Index + 1 -or- len(list) = count
            # Keep searching
        
        
        for i in range(1,len(big2DList)):
            print big2DList[i][0], #Print list of Directories containing search terms
            for x in range(1, len(big2DList[i])):
                print big2DList[i][x]
            #print("\n")
        

except KeyboardInterrupt:
    print "\nThanks for playing!"
exit(1)

# When found all you can find:
# Display Count, Path, Filename, Date in scrollable finder-type window, sortable by date, path, filename
# Ability to open file location from list selection And to open file from list selection if desired (like easyfind)

# Option to search within search results, search again with new term, save/print results? 




# Code to add widgets will go here...

