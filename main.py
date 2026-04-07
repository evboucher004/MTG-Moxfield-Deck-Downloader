# Import Module
from tkinter import *
from deckdl import deckdl
import subprocess
import os

# create root window
root = Tk()

# root window title and dimension
root.title("MTG Deck DL")
# Set geometry(widthxheight)
root.geometry('580x400')

root.rowconfigure(6, weight=1)


# adding a label to the root window
lbl = Label(root, text = "Moxfield Deck URL: ")
lbl.grid(column =0, row =1, pady=20, padx=15)

# adding Entry Field
urlBox = Entry(root, width=50)
urlBox.grid(column =1, row =1)

# adding Commander text box
dlCommander = Label(root, text = "Commander: ")
dlCommander.grid(column =1, row =3, pady=20)

# adding Successful Cards text box
dlCards = Label(root, text = "Cards: ")
dlCards.grid(column =1, row =4, pady=20)

# adding Successful Tokens text box
dlTokens= Label(root, text = "Tokens: ")
dlTokens.grid(column =1, row =5, pady=20)

# adding Download Result text box
dlResult = Label(root, text = " ")
dlResult.grid(column =1, row =7)

# function to display user text when
# button is clicked
def clicked():

    # Checks if URL entry field is empty
    if len(urlBox.get()) != 0:
        deck = deckdl()

        res = "Deck Downloaded Successfully"
        dlResult.configure(text = res)

        res = "Commander: " + deck.commander
        dlCommander.configure(text=res)

        res = "Cards: " + str(deck.successCount)
        dlCards.configure(text=res)

        res = "Tokens: " + str(deck.successTokenCount)
        dlTokens.configure(text=res)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.startfile(current_dir+"\images")

    else:
        res = "Deck Download Failed, Check URL"
        dlResult.configure(text=res)

# button widget with red color text inside
downloadbtn = Button(root, text = "Download Deck" , fg = "black", command=clicked)

# Set Button Grid
downloadbtn.grid(column=1, row=8, pady=20)

# Execute Tkinter
root.mainloop()