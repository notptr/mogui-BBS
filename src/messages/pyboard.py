#!/usr/bin/env python
#this is going the meassage board
#that I'm working on
#Programmer Matthew Deig

import os
import dataset
import yaml
from blessings import Terminal

def loadConfig(path):
    pass

def drawBoard(term):
    pass




if __name__ == "__main__":
    #load the terminal
    term = Terminal()
    
    #read config unless it isn't been made
    if os.access("/etc/pyboard.conf", os.F_OK):
        loadConfig("/etc/pyboard.conf")
    else:
        print(term.bold + term.red + "Please run the setup tool before using this program")
        
    #load database unless it isn't been made
