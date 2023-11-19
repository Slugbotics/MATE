import socket

s = socket.socket
print("socket created")

port = 12345
server = "192.168.1.177"
print("socket binded to %s" %(port))

s.bind(server, port)
s.listen(1)
print("socket is listening")
conn, addr = s.accept()
with conn:
    print("connected with ", addr)
while True:
    data = conn.recv(1024)
    if not data: break
    conn.sendall(data)





