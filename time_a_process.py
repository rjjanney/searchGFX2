from timeit import default_timer as timer
import subprocess

timeresults = []

def timeit(list_dir_command):
    
    start = timer()
    proc = subprocess.Popen(list_dir_command ,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for x in proc.stdout: pass
    end = timer()

    return(end - start) 


timeresults.append(timeit(["ls", "-lhoR", "/Volumes/GFX2/Graphics/MISC/AK"]))

timeresults.append(timeit(["ls", "-R", "/Volumes/GFX2/Graphics/MISC/AK"]))

print timeresults