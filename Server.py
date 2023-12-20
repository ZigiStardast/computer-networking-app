import logging
import socket
import threading
import datetime
import re

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
        try:
            while connected:
                if not logged:
                    self.socket.send(MENI_POCETNI.encode(FORMAT))
                    opcija = self.socket.recv(1024).decode(FORMAT)
                    if isinstance(opcija, str) and opcija == "!DISCONNECT":
                        print(f"Korisnik {self.address} se disconnect-ovao sa servera.")
                        break

                    if int(opcija) == 1:
                        print("[UPLATA HUMANITARNE POMOCI] Korisnik je izabrao opciju 1\n")
                        logged_to_send = "False"
                        self.socket.send(logged_to_send.encode(FORMAT))
                        uplata = self.uplata_humanitarne_pomoci(logged)
                        self.socket.send(uplata.encode(FORMAT))
                        print(f"Uplata korisnika {self.address}: {uplata}")
                    elif int(opcija) == 2:
                        print("[REGISTRACIJA KORISNIKA]\n")
                        registracija_info = self.registracija()
                        self.socket.send(registracija_info.encode(FORMAT))
                        print(f"Status registracije korisnika {self.address}: {registracija_info}")
                        if registracija_info == "Uspesna registracija!":
                            logged = True
                    elif int(opcija) == 3:
                        print("[PRIJAVA KORISNIKA]\n")
                        prijava_info = self.prijava()
                        self.socket.send(prijava_info.encode(FORMAT))
                        print(f"Status prijave korisnika {self.address}: {prijava_info}")
                        if prijava_info == "Korisnik se uspesno prijavio!":
                            logged = True
                    else:
                        print(f"Korisnik {self.address} je uneo pogresnu opciju!")
                if logged:
                    self.socket.send(MENI_NAKON_PRIJAVE.encode(FORMAT))
                    opcija = self.socket.recv(1024).decode(FORMAT)
                    if isinstance(opcija, str) and opcija == "!DISCONNECT":
                        print(f"Korisnik {self.address} se disconnect-ovao sa servera.")
                        break

                    if isinstance(opcija, str) and opcija == "!ODJAVA":
                        print(f"Korisnik {self.address} se odjavio sa servera.")
                        logged = False
                    elif int(opcija) == 1:
                        print("[UPLATA HUMANITARNE POMOCI] Korisnik je izabrao opciju 1\n")
                        logged_to_send = "True"
                        self.socket.send(logged_to_send.encode(FORMAT))
                        uplata = self.uplata_humanitarne_pomoci(logged)
                        self.socket.send(uplata.encode(FORMAT))
                        print(f"Uplata korisnika {self.address}: {uplata}")
                    elif int(opcija) == 4:
                        print("[Pregled ukupno skupljenih sredstava]\n")
                    elif int(opcija) == 5:
                        print("[Pregled transakcija]\n")
                    else:
                        print(f"Korisnik {self.address} je uneo pogresnu opciju!")
        except Exception as e:
            print("GRESKA!")
            logging.exception(e)

    def uplata_humanitarne_pomoci(self, logged: bool):
        print(f"Korisnik {self.address} salje podatke...")
        iznos = self.socket.recv(1024).decode(FORMAT)
        #print(f"Iznos: {iznos}")
        ime = self.socket.recv(1024).decode(FORMAT)
        #print(f"Ime: {ime}")
        prezime = self.socket.recv(1024).decode(FORMAT)
        #print(f"Prezime: {prezime}")
        adresa = self.socket.recv(1024).decode(FORMAT)
        #print(f"Adresa: {adresa}")
        if logged == False:
            broj_platne_kartice = self.socket.recv(1024).decode(FORMAT)
        else:
            broj_platne_kartice = "0"
        #print(f"Br. kartice: {broj_platne_kartice}")
        cvv_broj = self.socket.recv(1024).decode(FORMAT)
        #print(f"CVV: {cvv_broj}")
        vreme_uplate = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
        #print(f"Vreme uplate: {vreme_uplate}")

        try:
            if not credit_card_exists(broj_platne_kartice, cvv_broj):
                informacije_o_uplati = "Neuspelo placanje. Broj kartice koji je uneo korisnik ne postoji u bazi."
            elif not valid_amount_of_money(int(iznos)):
                informacije_o_uplati = "Neuspelo placanje. Korisnik je uneo manje od 200 dinara."
            else:
                broj_platne_kartice = find_card_with_cvv(cvv_broj)
                informacije_o_uplati = f"{ime} {prezime} {adresa} {broj_platne_kartice} {cvv_broj} {iznos} {vreme_uplate}\n"

                with open("spisak_uplata.txt", "a") as file:
                    file.write(informacije_o_uplati)
        except Exception as e:
            informacije_o_uplati = "GRESKA!"
            logging.exception(e)
        return informacije_o_uplati
    def registracija(self):
        global baza_kartica
        print(f"Korisnik {self.address} salje podatke...")
        username = self.socket.recv(1024).decode(FORMAT)
        #print(f"Username: {username}")
        password = self.socket.recv(1024).decode(FORMAT)
        #print(f"Password: {password}")
        ime = self.socket.recv(1024).decode(FORMAT)
        #print(f"Ime: {ime}")
        prezime = self.socket.recv(1024).decode(FORMAT)
        #print(f"Prezime: {prezime}")
        jmbg = self.socket.recv(1024).decode(FORMAT)
        #print(f"JMBG: {jmbg}")
        broj_platne_kartice = self.socket.recv(1024).decode(FORMAT)
        #print(f"Broj platne kartice: {broj_platne_kartice}")
        cvv = self.socket.recv(1024).decode(FORMAT)
        #print(f"Broj platne kartice: {cvv}")
        email = self.socket.recv(1024).decode(FORMAT)
        #print(f"E-MAIL: {email}")

        if username_exists(username):
            informacija = "Neuspesna registracija. Osoba sa istim username-om postoji!"
        else:
            if credit_card_exists(broj_platne_kartice,cvv):
                print("Korisnik se uspesno ulogovao!")
                informacija = "Uspesna registracija!"
                with open("spisak_korisnika.txt", 'a') as f:
                    f.write(f"{username},{password},{ime},{prezime},{jmbg},{broj_platne_kartice},{cvv},{email}\n")
            else:
                informacija = "Neuspesna registracija. Broj kartice nije ispravan!"

        return informacija

    def prijava(self):
        print(f"Korisnik {self.address} salje podatke...")
        username = self.socket.recv(1024).decode(FORMAT)
        #print(f"Username: {username}")
        password = self.socket.recv(1024).decode(FORMAT)
        #print(f"Password: {password}")

        if username_exists(username) == False or password_exists(password) == False:
            print("Neuspesna prijava!")
            informacija = "Korisnik se neuspesno prijavio."
        else:
            print("Uspesna prijava!")
            informacija = "Korisnik se uspesno prijavio!"

        return informacija

    def pregled_skupljenih_sredstava(self):
        pass

    def pregled_transakcija(self):
        pass

MENI_POCETNI = ("1) Uplata humanitarne pomoći\n"
                "2) Registracija\n"
                "3) Prijava")

MENI_NAKON_PRIJAVE = ("1) Uplata humanitarne pomoći\n"
                "4) Pregled ukupno skupljenih sredstava\n"
                "5) Pregled transakcija\n"
                "Dodatne opcije: !DISCONNECT, !ODJAVA")

def find_card_with_cvv(cvv:str):
    try:
        with open("baza_kartica.txt", 'r') as f:
            for linija in f:
                podaci = linija.strip().split(',')
                if podaci[1] == cvv:
                    broj_kartice = podaci[0]
                    return broj_kartice
    except FileNotFoundError:
        print(f"Fajl 'spisak_korisnika.txt' ne postoji. Kreiram novi fajl.")
        with open("spisak_korisnika.txt", 'w'):
            pass  # napravio prazan fajl
    return ""
def valid_credit_card(broj_kartice: str, cvv: str):
    pattern = re.compile(r'^\d{4}-\d{4}-\d{4}-\d{4}$')
    if pattern.match(broj_kartice) and 100 <= int(cvv) <= 999:
        return True
    else:
        return False
def valid_amount_of_money(money: int):
    if money < 200:
        return False
    return True
def credit_card_exists(broj_kartice: str, cvv: str):
    try:
        with open("baza_kartica.txt", 'r') as f:
            for linija in f:
                podaci = linija.strip().split(',')
                if broj_kartice == "0":
                    if podaci[1] == cvv:
                        return True
                else:
                    if podaci[0] == broj_kartice and podaci[1] == cvv:
                        return True
    except FileNotFoundError:
        print(f"Fajl 'spisak_korisnika.txt' ne postoji. Kreiram novi fajl.")
        with open("spisak_korisnika.txt", 'w'):
            pass  #napravio prazan fajl
    return False

def password_exists(password):
    try:
        with open("spisak_korisnika.txt", 'r') as f:
            for linija in f:
                podaci = linija.strip().split(',')
                if len(podaci) == 8 and podaci[1] == password:
                    return True
    except FileNotFoundError:
        print(f"Fajl 'spisak_korisnika.txt' ne postoji. Kreiram novi fajl.")
        with open("spisak_korisnika.txt", 'w'):
            pass  #napravio prazan fajl
    return False
def username_exists(username):
    try:
        with open("spisak_korisnika.txt", 'r') as f:
            for linija in f:
                podaci = linija.strip().split(',')
                if len(podaci) == 8 and podaci[0] == username:
                    return True
    except FileNotFoundError:
        print(f"Fajl 'spisak_korisnika.txt' ne postoji. Kreiram novi fajl.")
        with open("spisak_korisnika.txt", 'w'):
            pass  #napravio prazan fajl
    return False


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