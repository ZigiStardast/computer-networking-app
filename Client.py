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
            self.socket.send(opcija.encode(FORMAT))
            if opcija == "!DISCONNECT":
                print("Dovidjenja!")
                break

            if int(opcija) == 1:
                print("[UPLATA HUMANITARNE POMOCI]")
                logged_user = self.socket.recv(1024).decode(FORMAT)
                iznos = input("Unesite iznos: ")
                self.socket.send(iznos.encode(FORMAT))
                ime = input("Unesite ime: ")
                self.socket.send(ime.encode(FORMAT))
                prezime = input("Unesite prezime: ")
                self.socket.send(prezime.encode(FORMAT))
                adresa = input("Unesite adresu: ")
                self.socket.send(adresa.encode(FORMAT))
                br_kartice = input("Unesite br. kartice: ")
                self.socket.send(br_kartice.encode(FORMAT))
                cvv = input("Unesite cvv: ")
                self.socket.send(cvv.encode(FORMAT))

                informacije_o_uplati = self.socket.recv(1024).decode(FORMAT)
                print(f"Informacije o uplati: {informacije_o_uplati}")
            elif int(opcija) == 2:
                username = input("Unesite username: ")
                self.socket.send(username.encode(FORMAT))
                password = input("Unesite password: ")
                self.socket.send(password.encode(FORMAT))
                ime = input("Unesite ime: ")
                self.socket.send(ime.encode(FORMAT))
                prezime = input("Unesite prezime: ")
                self.socket.send(prezime.encode(FORMAT))
                jmbg = input("Unesite jmbg: ")
                self.socket.send(jmbg.encode(FORMAT))
                broj_platne_kartice = input("Unesite broj platne kartice: ")
                self.socket.send(broj_platne_kartice.encode(FORMAT))
                cvv = input("Unesite cvv: ")
                self.socket.send(cvv.encode(FORMAT))
                email = input("Unesite email: ")
                self.socket.send(email.encode(FORMAT))

                informacije_o_registraciji = self.socket.recv(1024).decode(FORMAT)
                print(f"Informacije o registraciji: {informacije_o_registraciji}")
            elif int(opcija) == 3:
                username = input("Unesite username: ")
                self.socket.send(username.encode(FORMAT))
                password = input("Unesite password: ")
                self.socket.send(password.encode(FORMAT))

                informacije_o_prijavi = self.socket.recv(1024).decode(FORMAT)
                print(f"Informacije o prijavi: {informacije_o_prijavi}")


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
