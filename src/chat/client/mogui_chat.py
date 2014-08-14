#!/usr/bin/env python

#The MIT License (MIT)
#Copyright (c) <2014> <Matthew Deig>
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from socket import *
from select import select
import getpass
import sys
from blessings import Terminal


HOST = ''
SERV = '192.168.1.103'
#USER = os.getlogin()
#USER = "notptr"

def drawBoard(term, messages):
    #print(term.clear)
    with term.location(0,0):
        for msg in messages:
            print(msg)

def run():
    receiver = socket(AF_INET, SOCK_STREAM)
    receiver.connect((HOST, 6666))
    messages = []
    term = Terminal()
    input = [sys.stdin, receiver]

    receiver.send(bytes("USERNAME "+getpass.getuser(), 'utf-8'))
    print(term.clear)
    while True:
        inputready, outputready, exceptready = select(input, [], [])
        quit = False
        
        for s in inputready:
            if s == receiver:
                data, addr = receiver.recvfrom(1024)
                messages.append(data.decode('utf-8'))
                drawBoard(term, messages)
            elif s == sys.stdin:
                msg = sys.stdin.readline()
                msg = msg.split("\n")

                if msg[0] == "!quit":
                    quit = True
                    break

                messages.append("<"+getpass.getuser()+"> "+msg[0])
                receiver.send(bytes(msg[0], 'utf-8'))
                drawBoard(term,messages)
            
        if quit:
            break
    
    receiver.close()
    print(term.clear)

if __name__ == "__main__":
    run()
