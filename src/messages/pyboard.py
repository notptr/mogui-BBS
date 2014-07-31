#!/usr/bin/env python
#this is going the meassage board
#that I'm working on
#Programmer Matthew Deig

import os
import dataset
import yaml
from blessings import Terminal

meassageDB = "bbs/messages/messages.db"
global pLocation

def showGroups(db):
    groups = db['groups']
    groups.all()

    for group in groups:
        print("[ "+term.yellow+str(group["gid"])+term.normal+" ] : "+term.white+group["name"]+term.normal)

def showGoto(db, term):
    with term.location():
        select = int(input(term.move_down + "What is your selection: "))
    return select 


def showGroup(db, gid, term):
    groupMsg = db['messages']
    findResults = groupMsg.find(gid=gid)

    for result in findResults:
        print("[ " + term.yellow + str(result['mid']) + term.normal + " ] | Topic: " + term.white + result['subject'] + term.normal + " | Author: " + term.white + result['msgStarter'] + term.normal)

def showMessage(db, gid, mid, term):
    topicMsg = db['messages']
    topics = topicMsg.find(gid=gid,mid=mid)
    
    for topic in topics:
        print(term.green + "Author: " + term.normal + topic['msgStarter'])
        print(term.green + "Topic: " + term.normal + topic['subject'])
        print(term.green + "Date: " + term.normal + topic['date'])
        print("------------------------")
        print()
        print()
        print(topic['message'])

def readReply(db, gid, mid, rid, term):
    topicMsgs = db['message']

    
    topics = topicMsgs.find(gid=gid, mid=mid)

    msgTitle = ""
    msgStarter = ""
    for topic in topics:
        msgTitle = topic['subject']
        msgStarter = topic['msgStarter']

    replyMsgs = db['reply']
    replys = replyMsgs.find(mid=mid, rid=rid)

    for reply in replys:
        print(term.green + "Orginal Author: " + term.normal + msgStarter)
        print(term.green + "Reply Author: " + term.normal + reply['rpyUser'])
        print(term.green + "RE: " + term.normal + msgTitle)
        print(term.green + "Date: " + term.normal + reply['date'])
        print("------------------------")
        print()
        print()
        print(reply['message'])




def showHelp():
    pass



def run(term):
    db = dataset.connect("sqlite:///"+meassageDB)

    location = "none"
    pLocation = "None"
    gid = 0
    mid = 0
    rid = 0

    while True:
        print(term.clear)
        print(term.blue + term.bold + "Welcome to the Message Boards"+term.normal)
        print()
        
        if location == "none":
            showGroups(db)
        elif location == "help":
            showHelp()
        elif location == "group":
            showGroup(db, gid, term)
        elif location == "message":
            rid = 0
            showMessage(db, gid, mid, term)
        elif location == "readReply":
            readReply(db, gid, mid, rid, term)
            rid = rid + 1
            location = "message"


        print()
        print()

        select = input("[ "+term.yellow + pLocation + term.normal +" : H-help, Q-Exit ] : ")

        if select == 'Q' or select == 'q':
            #show quiting meassage
            break
        elif select == "H" or select == 'h':
            location = "help"
            pLocation = "Help"
        elif select == "M" or select == "m":
            location = "none"
            pLocation = "None"
        elif select == "G" or select == "g":
            if location == "none":
                gid = showGoto(db, term)
                location = "group"
                pLocation = "Group"
            elif location == "group":
                mid = showGoto(db, term)
                location = "message"
                pLocation = "Messages"
        elif select == "B" or select == "b":
            if location == "message":
                location = "group"
                pLocation = "Group"
            elif location == "group":
                location = "none"
                pLocation = "None"
            elif rid > 0:
                location = "message"
        elif select == 'N' or select == 'n' and location == "message":
            location = "readReply"





if __name__ == "__main__":
    #load the terminal
    term = Terminal()

    if os.access(meassageDB, os.F_OK):
        run(term)
    else:
        print(term.red + "Please run the setup program")
        
    #load database unless it isn't been made
