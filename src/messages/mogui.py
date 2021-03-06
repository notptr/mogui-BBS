#!/usr/bin/env python

#The MIT License (MIT)
#
#Copyright (c) <2014> <Matthew Deig>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.




#this is going the meassage board
#that I'm working on
#Programmer Matthew Deig

import os
import datetime
import dataset
import yaml
from blessings import Terminal
#Added in for some fun not much else for it
from emoji import emojize
#FOR SQLITE ENABLE IF YOU PERFER IT
#meassageDB = "bbs/messages/messages.db"

meassageDB = "mysql://username:password@@hostname/database"
global pLocation

def showGroups(db):
    groups = db['groups']

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
        print("[ " + term.yellow + str(result['mid']) + term.normal + " ] | "+term.green+"Topic: " + term.white + emojize(result['subject']) + term.normal + " | "+term.green+"Author: " + term.white + result['msgStarter'] + term.normal)

def showMessage(db, gid, mid, term):
    topicMsg = db['messages']
    topics = topicMsg.find(gid=gid,mid=mid)
    
    for topic in topics:
        print(term.green + "Author: " + term.normal + topic['msgStarter'])
        print(term.green + "Topic: " + term.normal + emojize(topic['subject']))
        print(term.green + "Date: " + term.normal + topic['date'])
        print("------------------------------------------------------------------------------------------------------------")
        print()
        print()
        print(emojize(topic['message']))

def readReply(db, gid, mid, rid, term):
    topicMsgs = db['messages']

    
    topics = topicMsgs.find(gid=gid, mid=mid)

    msgTitle = ""
    msgStarter = ""
    for topic in topics:
        msgTitle = topic['subject']
        msgStarter = topic['msgStarter']

    replyMsgs = db['reply']
    replys = replyMsgs.find(mid=mid, rid=rid, gid=gid)

    for reply in replys:
        print(term.green + "Orginal Author: " + term.normal + msgStarter)
        print(term.green + "Reply Author: " + term.normal + reply['rpyUser'])
        print(term.green + "RE: " + term.normal + emojize(msgTitle))
        print(term.green + "Date: " + term.normal + reply['date'])
        print("------------------------------------------------------------------------------------------------------------")
        print()
        print()
        print(emojize(reply['message']))



def createMessage(db, term, gid):
    messages = db['messages']
    messageCount = db.query("SELECT MAX(mid) c FROM messages WHERE gid="+str(gid)+";")
    strMessage = ""
    mid = 0
    
    for msg in messageCount:
        if msg['c'] is None:
            mid = -1
        else:
            mid = int(msg['c'])
    mid = mid + 1
    
    subject = input(term.green + "Topic: " + term.normal)
    print(term.green+"Please type out your message and to stop please leave a . on a new line")
    print(term.green+"------------------------------------------------------------------------------------------------------------"+term.normal)
    
    while True:
        tempMessage = input()
        if tempMessage == ".":
            break
        else:
            strMessage = strMessage + tempMessage + "\n"
    if strMessage != "":
        messages.insert(dict(mid=mid, gid=gid, date=str(datetime.datetime.now()), subject=subject, message=strMessage, msgStarter=os.getlogin()))


def createReply(db, term, gid, mid):
    replys = db['reply']
    rpyCount = db.query("SELECT MAX(rid) c FROM reply WHERE gid="+str(gid)+" AND mid="+str(mid)+";")
    rid = 0
    strMessage = ""

    for rpy in rpyCount:
        if rpy['c'] is None:
            rid = -1
        else:
            rid = int(rpy['c'])
    rid = rid + 1
    

    print(term.green+"Please type out your message and to stop please leave a . on a new line")
    print(term.green+"------------------------------------------------------------------------------------------------------------"+term.normal)

    while True:
        tempMessage = input()
        if tempMessage == ".":
            break
        else:
            strMessage = strMessage + tempMessage +"\n"

    if strMessage != "":
        replys.insert(dict(rid=rid, mid=mid, gid=gid, date=str(datetime.datetime.now()), message=strMessage, rpyUser=os.getlogin()))


def createGroup(db, term):
    groups = db['groups']
    groupCount = db.query("SELECT MAX(gid) c FROM groups;")
    gid = 0

    for group in groupCount:
        if group['c'] is None:
            gid = -1
        else:
            gid = int(group['c'])
    gid = gid + 1
    
    newgroupname = input(term.green + "Name of the group: "+term.normal)
    if newgroupname != "":
        groups.insert(dict(gid=gid, name=newgroupname))

def addPrivUser(db, term):
    privuser = db['privuser']

    username = input(term.green+"Please enter in the user name for the privilege user: "+term.normal)
    
    if username != "":
        privuser.insert(dict(privuser=username))


def deleteMessages(db, term):
    select = input("Do you want to delete a group or a message and all the replies? [G/M] ")

    if select == 'g' or select == 'G':
        print("To delete a group pick the id to delete. hint it is the numbers to be pick to navagte to.")
        print(term.red+term.bold+"This will delete everything from the group"+term.normal)
        gid = int(input("What is the group id: "))
        print(term.red+term.bold+"DELETEING ALL THE MESSAGES AND REPLIES OUT OF THIS GROUP"+term.normal)
        reply = db['reply']
        reply.delete(gid=gid)

        messages = db['messages']
        messages.delete(gid=gid)

        groups = db['groups']
        groups.delete(gid=gid)
        print(term.green+"Deletion has been completed."+term.normal)


    elif select == 'M' or select == 'M':
        print("To delete a message you need to give the id of the message and the group id. hint it is the number used to navgate to.")
        print(term.red+term.bold+"THIS WILL ONLY DELETE THE MESSAGE AND REPLIES."+term.normal)

        gid = int(input("Group ID: "))
        mid = int(input("Message ID: "))

        messages = db['messages']
        messages.delete(gid=gid,mid=mid)

        reply = db['reply']
        reply.delete(gid=gid,mid=mid)

        print(term.green+"Deletion has been completed"+term.normal)


def removePrivUser(db, term):
    print("This will remove a user out of the privilege status")
    username = input("What is the user you want to remove: ")

    user = db['privuser']
    user.delete(privuser=username)


def showHelp(term, privUser):
        print("Welcome to the commands of the board")
        print(term.red+"Q"+term.normal+" is for exiting the board program")
        print(term.red+"G"+term.normal+" is used to goto a group and messages")
        print(term.red+"H"+term.normal+" is here")
        print(term.red+"B"+term.normal+" is used to navgate back a menu.")
        print(term.red+"N"+term.normal+" is used to view the next reply in a message")
        print(term.red+"C"+term.normal+"  or"+term.red+" R"+term.normal+"  is used to make a topic or reply to a topic in the groups or the messages")
        print(term.red+"M"+term.normal+"  is for getting back to the main menu")
        print()
        
        if privUser:
            showPrivHelp(term)
    
def showPrivHelp(term):
    print()
    print("Welcome to the privilege commands")
    print(term.red+"CG"+term.normal+" is to create a group at the None stage of the board")
    print(term.red+"D"+term.normal+" is used to delete groups and messages. This is permanent")
    print(term.red+"AP"+term.normal+" is used to make a user name a admin of the board - use the system's username")
    print(term.red+"RP"+term.normal+" is used to remove the admin status of a users - use the system's username")


def run(term):
    specialUsers = []
    #db = dataset.connect("sqlite:///"+meassageDB)
    db = dataset.connect(meassageDB)
    privusers = db['privuser']

    for privuser in privusers:
        specialUsers.append(privuser['privuser'])


    location = "none"
    pLocation = "None"
    gid = 0
    mid = 0
    rid = 0
    
    print(term.clear)
    print(term.blue + term.bold + "Welcome to the Message Boards"+term.normal)
    print()

    while True:
        
        if location == "none":
            showGroups(db)
        elif location == "help":
            if os.getlogin() in specialUsers:
                showHelp(term, True)
            else:
                showHelp(term, False)
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
            elif location == "help":
                location = "none"
                pLocation = "None"
        elif select == 'N' or select == 'n' and location == "message":
            location = "readReply"
        elif select == 'C' or select == 'c' or select == 'R' or select == 'r':
            if location == "group":
                createMessage(db, term, gid)
            elif location == "message":
                createReply(db, term, gid, mid)
        if os.getlogin() in specialUsers:
            if select == 'cg' or select == 'CG' and location == "none":
                createGroup(db, term)
            elif select == 'd' or select == 'D':
                deleteMessages(db, term)
            elif select == 'ap' or select == 'AP' and location == "none":
                addPrivUser(db, term)
            elif select == 'rp' or select == 'RP' and location == "none":
                removePrivUser(db, term)

        print(term.clear)






if __name__ == "__main__":
    #load the terminal
    term = Terminal()

    #if os.access(meassageDB, os.F_OK):
    run(term)
    print(term.clear)
    #else:
    #    print(term.red + "Please run the setup program")
        
    #load database unless it isn't been made
