import socket

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect(("172.24.112.1", port))  # connect to the server

    # message = input(" -> ")  # take input

    # while message.lower().strip() != 'bye':
    #     client_socket.send(message.encode())  # send message
    #     data = client_socket.recv(1024).decode()  # receive response

    #     print('Received from server: ' + data)  # show in terminal

    #     message = input(" -> ")  # again take input
    filename = input (" (filename)-> ")
    filetosend = open(filename, "rb")
    data = filetosend.read(1024)
    while data:
        print("Sending...")
        client_socket.send(data)
        data = filetosend.read(1024)
    filetosend.close()
    client_socket.send(b"DONE")
    print("Done Sending.")
    # print(client_socket.recv(1024))


    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()