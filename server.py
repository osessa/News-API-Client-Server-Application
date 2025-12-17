import socket
import threading

#                (IP +  Port Number)
SERVER_ADDRESS = ("127.0.0.1", 50555)

# create the socket and this socket have ("AF_INET": Address Family Internet = IPv4, TCP "SOCK_STREAM")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# link the server address with the socket throgh (bind)
server_socket.bind(SERVER_ADDRESS)

# the server will keep one user waite if the server busy
server_socket.listen(1)

# to know when server start for (Debuging)
print(f"Server listening on {SERVER_ADDRESS} ...")

while True:
    # make the server wait for clients to connect (bloking)
    connection, address = server_socket.accept()
    # main thread
    client_thread = threading.Thread(target=handle_client, args=(connection, address))
    # start the thread and go back on the loop again to wait another client
    client_thread.start()
