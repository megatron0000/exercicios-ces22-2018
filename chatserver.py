#!/usr/bin/env python
import socket
from time import ctime
from queue import Queue
from threading import Thread


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.queue = Queue()
        self.clients = []

    def listen(self):
        self.sock.listen(5)
        Thread(target=self.broadcast_loop).start()
        while True:
            client, address = self.sock.accept()
            self.clients.append(client)
            client.settimeout(60)
            Thread(target=self.listen_to_client, args=(client,)).start()

    def listen_to_client(self, client):
        size = 1024

        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the received data
                    msgstr = data.decode('utf-8')
                    print(msgstr)
                    self.push_to_queue((ctime() + ' ' + msgstr).encode('utf-8'))
                else:
                    self.clients.remove(client)
                    raise RuntimeError('Client disconnected')
            except:
                client.close()
                self.clients.remove(client)
                print("Exception")
                return False

    def broadcast_loop(self):
        while True:
            data = self.queue.get(block=True)
            for client in self.clients:
                client.send(data)

    def push_to_queue(self, raw_msg):
        self.queue.put(raw_msg)


if __name__ == "__main__":
    while True:
        port_num = input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass
    ThreadedServer('', port_num).listen()
