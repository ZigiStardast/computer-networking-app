import socket
import threading
import logging
import time

class ListenThread(threading.Thread):
    def __init__(self, comm_socket):
        self.socket = comm_socket

        super().__init__()
        self.start()

    def run(self):
        while True:
            pregled_meni = self.socket.recv(1024).decode(FORMAT)
            print(pregled_meni)
            opcija = input("Unesite zeljenu opciju: ")
            self.socket.send(opcija)
            if opcija == "!DISCONNECT":
                break

            if opcija == 1:
                #ovde salji redom ime prezime itd. prvo input



HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
FORMAT = "utf-8"
comm_socket = None

def start():
    global comm_socket
    while True:
        try:
            comm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            comm_socket.connect((HOST, PORT))

            listener = ListenThread(comm_socket)
            break
        except Exception as e:
            logging.exception(e)
            print("Ne moze se povezati na server...")
            print("Pokusaj za 5 sekundi...")
            time.sleep(5)

start()
