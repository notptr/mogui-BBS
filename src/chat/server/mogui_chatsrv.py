#!/usr/bin/env python

import socket, select

listeners = []
messages = []
usernames = {}



def run():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    serv.bind(('',6666))
    serv.setblocking(0)

    serv.listen(5)

    while True:
        
        read, write, error = select.select([serv]+listeners, listeners, [], 60)

        for sock in read:
            if sock is serv:
                handle_Connection(serv)
            else:
                handle_Read(sock)

        for sock in write:
            for msg in messages:
                if sock != msg[1]:
                    sock.send(msg[0])
        messages.clear()

    
    serv.close()



def handle_Connection(sock):
    newClient = sock.accept()
    print("New client")
    listeners.append(newClient[0])
    print(listeners)

def handle_Read(sock):
    msg = sock.recv(1024)

    strmsg = msg.decode('utf-8')
    strmsgsplit = strmsg.split()
    
    if len(msg) == 0:
        print("client closed")
        sock.close()
        listeners.remove(sock)
    elif strmsgsplit[0] == "USERNAME":
        usernames[sock] = strmsgsplit[1]
        messages.append([bytes(strmsgsplit[1] + " has entered the room.", 'utf-8'), 0])
    else:
        print(strmsg)
        strmsg = "<" + usernames[sock] + "> " + strmsg
        messages.append([bytes(strmsg, 'utf-8'), sock])

if __name__ == "__main__":
    run()
