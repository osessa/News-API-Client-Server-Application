import socket
import threading


# handle the client thread function
def handle_client(connection, address):
    # announce new client connection
    print(f"[+] New client connected {address}")
    
    # auto close connection by use 'with'
    with connection:
        try:
            # send and recive data loop
            while True:
                # recive data from client
                data = connection.recv(1024)
                if not data:
                    break
                # print recived data
                print(f"[{address}] : {data.decode('ascii')}")
                # send recived data back to client
                connection.sendall(data)
            # exit the loop when client disconnects

        except ConnectionResetError:
            print(f"[!] Client {address} disconnected unexpectedly")
        
    # announce client disconnection
    print(f"[-] Client disconnected {address}")


#                (IP +  Port Number)
SERVER_ADDRESS = ("127.0.0.1", 50555)

# create the socket and this socket have ("AF_INET": Address Family Internet = IPv4, TCP "SOCK_STREAM")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# link the server address with the socket throgh (bind)
server_socket.bind(SERVER_ADDRESS)

# the server will keep one user waite if the server busy
server_socket.listen(1)

# announce server start for (Debuging)
print(f"Server listening on {SERVER_ADDRESS} ...")

while True:
    # make the server wait for clients to connect (bloking)
    connection, address = server_socket.accept()
    # create new thread for the client
    client_thread = threading.Thread(target=handle_client, args=(connection, address))
    # start the thread and go back on the loop again to wait another client
    client_thread.start()
