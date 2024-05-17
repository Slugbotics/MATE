import socket

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect(("192.168.4.1", port))  # connect to the server

    filetodown = open("test_wortk.txt", "wb+")
    file_content = client_socket.recv(20)
    while True:
        while (file_content):
            filetodown.write(file_content)
            file_content = client_socket.recv(20)
            print(file_content)
        filetodown.close()
        data = client_socket.recv(20)
        if data == b"DONE":
            print("Done Receiving")
            break
    client_socket.close()
    

if __name__ == '__main__':
    client_program()
