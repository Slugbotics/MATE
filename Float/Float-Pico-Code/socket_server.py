import socket

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind(("172.24.112.1", port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    filetodown = open("test2.txt", "wb") ####!!!

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        print("Recieving...")
        data = conn.recv(1024)
        if data == b"DONE":
            print("Done Receiving.")
            break
        # print("from connected user: " + str(data))
        filetodown.write(data)
    filetodown.close()
    # conn.send("Thanks for connecting")
    server_socket.close()
    # conn.send(data.encode())  # send data to the client
    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()