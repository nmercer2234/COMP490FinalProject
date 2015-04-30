__author__ = 'Nicole Mercer nmercer@student.bridgew.edu'

from Tkinter import *

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

entryButton = Button(top, text = "Print", command= lambda: printEnteredText(textBox.get()), height = 3, width = 10, activebackground = "red")
entryButton.place(x=550, y=335)

topLeftButton = Button(top, text = "Button 1", command= lambda: printCoordinates(0,0), height = 5, width = 10, activebackground = "red")
topLeftButton.place(x=0, y=0)

topRightButton = Button(top, text = "Button 2", command= lambda: printCoordinates(952,0), height = 5, width = 10, activebackground = "red")
topRightButton.place(x=922, y=0)

bottomLeftButton = Button(top, text = "Button 3", command= lambda: printCoordinates(0,575), height = 5, width = 10, activebackground = "red")
bottomLeftButton.place(x=0, y=515)

bottomRightButton = Button(top, text = "Button 4", command= lambda: printCoordinates(952,575), height = 5, width = 10, activebackground = "red")
bottomRightButton.place(x=922, y=515)

top.mainloop()