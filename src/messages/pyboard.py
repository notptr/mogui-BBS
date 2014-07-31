#!/usr/bin/env python
#this is going the meassage board
#that I'm working on
#Programmer Matthew Deig

import os
import dataset
import yaml
from blessings import Terminal

meassageDB = "bbs/messages/messages.db"


def run(term):
    db = dataset.connect("sqlite:///"+meassageDB)
    location = "None"
    while True:
        groups = db['groups']

        print(term.blue + term.bold + "Welcome to the Message Boards"+term.normal)
        
        for group in groups:
            print("[ "+term.yellow+str(group["gid"])+term.normal+" ] : "+term.white+group["name"]+term.normal)

        print()
        print()

        print("[ "+term.yellow + location + term.normal +" : H-help ] :")
        break




if __name__ == "__main__":
    #load the terminal
    term = Terminal()

    if os.access(meassageDB, os.F_OK):
        run(term)
    else:
        print(term.red + "Please run the setup program")
        
    #load database unless it isn't been made
