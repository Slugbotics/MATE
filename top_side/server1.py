import socket
import threading

HEADER = 64 #tells first message needs to be of length 64
PORT = 23

#IPv4
# SERVER = "169.233.155.123"

#Alternate way to get the IPv4
SERVER = socket.gethostbyname(socket.gethostname())
#SERVER = "192.168.1.177"


ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


print(socket.gethostname())  #gets the host name


# tells what type of address we are looking for
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)  #anything that connects will hit the socket


#handles the individual connections between server and client
#ensures other clients aren't blocked from connecting
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True

    #waits until a connection
    while connected:
        #blocking line: wont pass until a message is received from client
        
        #decodes the format of header into the utf-8 format
        msg_length = conn.recv(HEADER).decode(FORMAT)  #how long is incoming message

        #if the message has anything, when we connect and receive nothing
        if msg_length:
            msg_length = int(msg_length)    #convert to int
            msg = conn.recv(msg_length).decode(FORMAT)  #put as how many bytes we are receiving

            if msg == DISCONNECT_MESSAGE:
                connected = False


            print(f"[{addr}] {msg}")

    conn.close() #cleanly disconnect



 

def start():
    #server.listen() # listen for new connections

    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        data, addr = server.recvfrom(1024) 

        # wait for a new connection to the server, stores the IP address and the port it came from
        thread = threading.Thread(target = handle_client, args = (data, addr))
        thread.start()
        
        #tells how many threads are active, represents clients connected
        # -1 accounts for the constantly active connection
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")



print("[STARTING] server is starting...")
start()
