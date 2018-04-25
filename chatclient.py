#!/usr/bin/env python
from socket import *
from threading import Thread

HOST = '127.0.0.1'  # or 'localhost'
PORT = 21567
BUFSIZ = 1024
tcpCliSock = socket(AF_INET, SOCK_STREAM)
ADDR = (HOST, PORT)
tcpCliSock.connect(ADDR)
host = tcpCliSock.getsockname()  # print client host name
print(host)


def receive_loop():
    while True:
        incoming = tcpCliSock.recv(BUFSIZ)
        if not incoming:
            break
        print(incoming.decode('utf-8'))


Thread(target=receive_loop).start()

while True:
    data = (input('> ')).encode('utf-8')
    if not data:
        break
    tcpCliSock.send(data)


# tcpCliSock.close() Inútil !
