filenames = ['/Volumes/GFX2/Graphics/MISC/Lists/FileList.txt', '/Volumes/GFX2/Graphics/MISC/Lists/_FileList.txt', '/Volumes/GFX2/Graphics/MISC/Lists/ME_FileList.txt']
with open('/Volumes/GFX2/Graphics/MISC/Lists/FileList_Cct.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)