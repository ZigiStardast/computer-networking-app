import socket
import threading
import datetime

class ClientHandler(threading.Thread):
    def __init__(self, comm_socket, cl_address):
        self.socket = comm_socket
        self.address = cl_address

        super().__init__()
        self.start()

    def run(self):
        print(f"[KONEKCIJA] Korisnik {self.address} se povezao na server!")
        connected = True
        logged = False
        while connected:
            if not logged:
                self.socket.send(MENI_POCETNI)
                opcija = self.socket.recv(1024).decode(FORMAT)
                if opcija == 1:
                    self.uplata_humanitarne_pomoci()

    def uplata_humanitarne_pomoci(self):
        #ime, prezime, adresu, broj platne kartice i CVV broj (trocifren broj) i iznos
        ime = self.socket.recv(1024).decode(FORMAT)
        prezime = self.socket.recv(1024).decode(FORMAT)
        adresa = self.socket.recv(1024).decode(FORMAT)
        broj_platne_kartice = self.socket.recv(1024).decode(FORMAT)
        cvv_broj = self.socket.recv(1024).decode(FORMAT)

        vreme_uplate = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
        informacije_o_uplati = f"{ime} {prezime} {adresa} {broj_platne_kartice} {cvv_broj} {vreme_uplate}\n"

        with open("spisak_uplata.txt", "a") as file:
            file.write(informacije_o_uplati)

    def registracija(self):
        pass

    def prijava(self):
        pass

    def pregled_skupljenih_sredstava(self):
        pass

    def pregled_transakcija(self):
        pass

MENI_POCETNI = ("1) Uplata humanitarne pomoći\n"
                "2) Registracija\n"
                "3) Prijava")

MENI_NAKON_PRIJAVE = ("1) Uplata humanitarne pomoći\n"
                "2) Pregled ukupno skupljenih sredstava\n"
                "3) Pregled transakcija")


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
FORMAT = "utf-8"

def start():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #koristi ipv4 adresu, data se strimuje kroz soket
    server_socket.bind((HOST, PORT))

    server_socket.listen(5) #red cekanja 5
    while True:
        print(f"[CEKANJE] Server {HOST} ceka na konekciju!")
        comm_socket, cl_address = server_socket.accept()
        client = ClientHandler(comm_socket, cl_address)

start()