#!/usr/bin/env python

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
