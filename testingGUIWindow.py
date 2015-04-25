__author__ = 'Nicole Mercer nmercer@student.bridgew.edu'

from tkinter import *

top = Tk()
top.geometry("1000x600")

var = StringVar()
coordLabel = Label(top, textvariable=var)
coordLabel.place(x=465, y=320)

def printCoordinates(x, y):
    setting = "(", top.winfo_rootx()+x, ",", top.winfo_rooty()+y, ")" #coordinates relative to screen
    #setting = "(", x, ",", y, ")" #use this if you only want coordinates relative to the window
    var.set(setting)

textBox = Entry(top)
textBox.place(x=428, y=350)

def printEnteredText(enteredText):
    var.set(enteredText)
    textBox.delete(0,len(enteredText))

entryButton = Button(top, text = "Print", command= lambda: printEnteredText(textBox.get()))
entryButton.place(x=550, y=347)

topLeftButton = Button(top, text = "demo", command= lambda: printCoordinates(0,0))
topLeftButton.place(x=0, y=0)

topRightButton = Button(top, text = "demo2", command= lambda: printCoordinates(952,0))
topRightButton.place(x=952, y=0)

bottomLeftButton = Button(top, text = "demo3", command= lambda: printCoordinates(0,575))
bottomLeftButton.place(x=0, y=575)

bottomRightButton = Button(top, text = "demo4", command= lambda: printCoordinates(952,575))
bottomRightButton.place(x=952, y=575)

top.mainloop()