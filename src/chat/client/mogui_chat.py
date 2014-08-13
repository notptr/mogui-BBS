#!/usr/bin/env python

from socket import *
from select import select
import getpass
import sys


HOST = ''
SERV = '192.168.1.103'
#USER = os.getlogin()
USER = "notptr"

def run():
    receiver = socket(AF_INET, SOCK_STREAM)
    receiver.connect((HOST, 6666))
    input = [sys.stdin, receiver]

    receiver.send(bytes("USERNAME "+getpass.getuser(), 'utf-8'))

    while True:
        inputready, outputready, exceptready = select(input, [], [])

        for s in inputready:
            if s == receiver:
                data, addr = receiver.recvfrom(1024)
                print(data.decode('utf-8'))
            elif s == sys.stdin:
                receiver.send(bytes(sys.stdin.readline(), 'utf-8'))
    
    receiver.close()

if __name__ == "__main__":
    run()
