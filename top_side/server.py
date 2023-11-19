import socket

s = socket.socket()
print("socket created")

port = 12345
server = ''
print("socket binded to %s" %(port))

s.bind((server, port))
s.listen(1)
print("socket is listening")
conn, addr = s.accept()
with conn:
    print("connected with ", addr)
while True:
    data = conn.recv(1024)
    if not data: break
    conn.sendall(data)





