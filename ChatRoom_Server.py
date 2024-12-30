#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

ENCODING_METHOD = "utf8"
BUFSIZ = 1024

# Invia un messaggio ad uno specifico client
def SendMessageToClient(client, message):
    client.send(bytes(message, ENCODING_METHOD))

# Invia un messaggio a tutti i client connessi
def BroadcastMessageString(message, prefix = ""):
    for utente in clients:
        utente.send(bytes(prefix + message, ENCODING_METHOD))

# Invia un messaggio a tutti i client connessi
def BroadcastMessageBytes(message, prefix = ""):
    for utente in clients:
        utente.send(bytes(prefix, ENCODING_METHOD) + message)

# Gestisce e accetta le connnessioni dei Client in entrata
def AcceptIncomingConnections():
    while True:
        client, clientAddress = SERVER.accept()
        print("%s:%s si è collegato." % clientAddress)

        # Invio del primo messaggio al Client appena connesso
        SendMessageToClient(client, "Ciao! Per iniziare, digita il tuo nome!")

        # Registrazione del Client
        addresses[client] = clientAddress

        # Creazione di un Thread per ciascun Client
        thread = Thread(target = HandleClient, args = (client,))
        thread.start()
        

# Gestisce la connessione di un singolo Client
def HandleClient(client):
    try:
        # Creazione e invio del messaggio di benvenuto al nuovo Client
        name = client.recv(BUFSIZ).decode("utf8")
        welcomeMessage = 'Benvenuto [%s]!' % name
        client.send(bytes(welcomeMessage, "utf8"))
        msg = "[%s] si è unito all chat!" % name

        # Invio a tutti i Client connessi di un messaggio che notifica l'entrata di questo nuovo Client
        BroadcastMessageString(msg)

        # Aggiornamento del dizionario dei client
        clients[client] = name
    except Exception:
        return
    
    # Loop che consente di mettersi in ascolto dei messaggi inviati da questo Client
    while True:
        try:
            # Ricezione del messaggio dal Client
            msg = client.recv(BUFSIZ)
            if msg == bytes("{quit}", "utf8"):
                # Se il messaggio è di tipo "quit", il Client si è disconnesso e lo si notifica agli altri
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                BroadcastMessageString("[%s] ha abbandonato la Chat." % name)
                break
            else:
                # Altrimenti, si manda il messaggio ricevuto a tutti i Client connessi
                BroadcastMessageBytes(msg, "[" + name + "]" + ": ")
        except ConnectionError:
            # Gestione dell'abbandono imprevisto del Client
            client.close()
            del clients[client]
            BroadcastMessageString("[%s] ha abbandonato la Chat." % name)
            break
        
# Creazione strutture dati necessarie
clients = {}
addresses = {}

HOST = ''
PORT = 53000
ADDR = (HOST, PORT)

# Avvio del server in ascolto delle richieste di connessione dei Client
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target = AcceptIncomingConnections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
