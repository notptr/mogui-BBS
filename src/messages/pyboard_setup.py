#!/usr/bin/env python
#this is going the intialsetup for the meassage board
#that I'm working on
#Programmer Matthew Deig

import os
import dataset
import yaml
from blessings import Terminal

def writeConfig(path):
    pass

def loadConfig(path):
    pass

def drawBoard(term):
    pass




if __name__ == "__main__":
    #read config unless it isn't been made
    if os.access("/etc/pyboard.conf", os.F_OK):
        writeConfig("/etc/pyboard.conf")
    else:
        loadConfig("/etc/pyboard.conf")
    #load database unless it isn't been made
    #make the terminal
    
