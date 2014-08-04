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
    #if os.access("bbs/messages/messages.db", os.F_OK):
    #    print(term.green + "Database has been already setup no need to run this agian."+term.normal)
    #else:
        #THIS IS FOR SQLITE IF YOU WANT IT ENABLE IT
        #print("Making directories")
        #os.mkdir("bbs")
        #os.mkdir("bbs/messages")
        #open("bbs/messages/messages.db", "a").close()


    print("Making database")
        #FOR SQLITE ENABLE IT IF YOU WANT IT
        #db = dataset.connect("sqlite:///bbs/messages/messages.db")
        
    db = dataset.connect("mysql://username:password@@hostname/database")

    print("Making tables")
    tablesInit(db)
        
        #THIS IS FOR SQLITE IF YOU WANT ENABLE IT
        #os.chmod("bbs/messages/messages.db", 0o666)

    print(term.green + "Database has been created and is ready to go."+term.normal)
