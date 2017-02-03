from Tkinter import Tk
from tkFileDialog import askopenfilename

Tk().withdraw() 
filename = askopenfilename() 
print(filename) 