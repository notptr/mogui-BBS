#!/usr/bin/env python
#this is going the intialsetup for the meassage board
#that I'm working on
#Programmer Matthew Deig

import os
import datetime
import dataset
from blessings import Terminal


def tablesInit(database):
    groups = database['groups']
    groups.insert(dict(gid=0,name="General"))

    messages = database['messages']
    messages.insert(dict(mid=0,gid=0,date=str(datetime.datetime.now()),subject="Welcome",message="Welcome to mogui and this your first setup. That is why you are seeing this", msgStarter="mogui"))

    reply = database['reply']
    reply.insert(dict(rid=0,mid=0,gid=0,date=str(datetime.datetime.now()),message="This is how a reply would look in the board area", rpyUser="mogui"))

    privUser = database['privuser']
    print("Adding privilege Users to the database")
    
    while True:
        username = input("What user do you want to use (Leave blank to use this user "+os.getlogin()+" or type a *inx user name instead)")

        if username == "":
            username = os.getlogin()

        print("Adding user to database")
        privUser.insert(dict(privuser=username))

        answer = input("Do you want to add another user to the database [Y/N] ")

        if answer != "Y" or answer != "y":
            break



if __name__ == "__main__":
    term = Terminal()
    #load database unless it isn't been made

    #change this if you want it in a different place or just run it as it own
    #user
    if os.access("bbs/messages/messages.db", os.F_OK):
        print(term.green + "Database has been already setup no need to run this agian.")
    else:
        print("Making directories")
        os.mkdir("bbs")
        os.mkdir("bbs/messages")
        open("bbs/messages/messages.db", "a").close()


        print("Making database")
        db = dataset.connect("sqlite:///bbs/messages/messages.db")

        print("Making tables")
        tablesInit(db)

        os.chmod("bbs/messages/messages.db", 0o666)

        print(term.green + "Database has been created and is ready to go.")
