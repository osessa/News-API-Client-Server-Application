import socket

#                (IP +  Port Number)
SERVER_ADDRESS = ("127.0.0.1", 50555)
# create the socket and this socket have (IPv4 "AF_INET" , TCP "SOCK_STREAM")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# link the server address with the socket throgh (bind)
server_socket.bind(SERVER_ADDRESS)

# the server will keep one user waite if the server busy
server_socket.listen(1)

# to know when server start for (Debuging)
print(f"Server listening on {SERVER_ADDRESS} ...")

# make the server wait for clients to connect
connection, address = server_socket.accept()

# recive data from clients (data size=  1024 byte)
data = connection.recv(1024)

# translate bytes into string
print(data.decode("ascii"))
