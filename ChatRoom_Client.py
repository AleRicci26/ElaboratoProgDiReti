#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

ENCODING_METHOD = "utf8"
FONT = ("Arial", 14)
BUFSIZ = 1024

# Gestisce la ricezione dei messaggi dal server
def Receive():
    while True:
        try:
            # Ricezione dei messaggi in arrivo dal server
            message = clientSocket.recv(BUFSIZ).decode(ENCODING_METHOD)
            # Inserimento del messaggio ricevuto nella lista locale
            messageList.insert(tkt.END, message)
        except Exception:
            break

# Gestisce l'invio dei messaggi al server
def Send(event = None):
    try:
        # Ottenimento del messaggio dal campo della GUI
        message = messageVar.get()
        # Pulizia del campo della GUI
        messageVar.set("")
        # Invio del messaggio sul server attraverso il socket
        clientSocket.send(bytes(message, ENCODING_METHOD))
    except Exception:
        return

# Gestisce la connessione con il server
def Connect():
    try:
        # Creazione dell'indirizzo (nome, porta)
        address = (server.get(), int(port.get()))

        # Connession effettiva
        clientSocket.connect(address)

        # Creazione del Thread per la ricezione dei messaggi dal server
        receiveThread = Thread(target = Receive)
        receiveThread.start()

        # In caso di connessione avvenuta con successo, Show della pagina della ChatRoom
        chatroomPage.lift()
    except OSError as e:
        connectionPageError.set("[Errore Connessione]\r\n" + str(e))
    except Exception as e:
        connectionPageError.set("[Errore]\r\n" + str(e))

# Gestisce la disconnessione e la chisura dell'applicazione
def Quit(event = None):
    try:
        # Invio di un messaggio per notificare il server della volonta' di disconnesione
        clientSocket.send(bytes("{quit}", ENCODING_METHOD))
        clientSocket.close()

        # Chiusura dell'applicazione
        root.quit()
    except Exception:
        root.quit()

# Creazione della finestra
root = tkt.Tk()
root.title("Chat Client-Server")
root.geometry("500x600")
root.resizable(False, False)

# Creazione delle pagine di connesione e di ChatRoom
connectionPage = tkt.Frame(root, padx = 5, pady = 150)
chatroomPage = tkt.Frame(root, padx = 5, pady = 5)

connectionPage.place(in_ = root, x = 0, y = 0, relwidth = 1, relheight = 1)
chatroomPage.place(in_ = root, x = 0, y = 0, relwidth = 1, relheight = 1)

# Creazione dei campi che ospiteranno il nome del server e la porta per la connessione
server = tkt.StringVar()
serverField = tkt.Entry(connectionPage, textvariable = server, font = FONT)
serverField.pack()

port = tkt.StringVar()
portField = tkt.Entry(connectionPage, textvariable = port, font = FONT)
portField.pack(pady = 5)

# Creazione del pulsante per la connessione
connectButton = tkt.Button(connectionPage, text="Connetti", font = FONT, command = Connect)
connectButton.pack()

connectionPageError = tkt.StringVar()
connectionPageErrorField = tkt.Message(connectionPage, textvariable = connectionPageError, width = 500)
connectionPageErrorField.pack(pady = 5)

connectionPage.lift()

# Creazione del frame per contenere i messaggi
messageFrame = tkt.Frame(chatroomPage)
messageVar = tkt.StringVar()
scrollbar = tkt.Scrollbar(messageFrame)

# Creazione della lista effettiva di messaggi
messageList = tkt.Listbox(messageFrame, height = 20, width = 100, yscrollcommand = scrollbar.set, font = FONT)
scrollbar.pack(side = tkt.RIGHT, fill = tkt.Y)
messageList.pack(side = tkt.LEFT, fill = tkt.BOTH)
messageList.pack()
messageFrame.pack()

# Creazione del campo che ospiterà il messaggio
messageField = tkt.Entry(chatroomPage, textvariable = messageVar, width = 100, font = FONT)

# Collegamento dell tasto "Invio" all'azione di invio del messaggio
messageField.bind("<Return>", Send)
messageField.pack(pady = 5)

# Creazione pulsanti di invio messaggio e disconnessione
sendButton = tkt.Button(chatroomPage, text = "Invia Messaggio", font = FONT, command = Send)
quitButton = tkt.Button(chatroomPage, text = "Disconnetti", font = FONT, command = Quit)
sendButton.pack()
quitButton.pack(pady = 5)

# Collegamento dell'azione di chiusura della finestra alla funzione di disconnessione
root.protocol("WM_DELETE_WINDOW", Quit)

# Creazione del Socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Impostazione di server e porta di default
server.set("localhost")
port.set("53000")

# Avvio dell'applicazione
tkt.mainloop()
