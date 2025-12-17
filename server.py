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
                print(f"[{address}] : {data.decode('utf-8')}")
                # send recived data back to client
                connection.sendall(data)
            # exit the loop when client disconnects

        except ConnectionResetError:
            print(f"[!] Client {address} disconnected unexpectedly")
        except Exception as e:
            print(f"[!] Error with Client {address}: {e}")

    # announce client disconnection
    print(f"[-] Client disconnected {address}")


#                (IP +  Port Number)
SERVER_ADDRESS = ("127.0.0.1", 50555)

# create the socket and this socket have ("AF_INET": Address Family Internet = IPv4, TCP "SOCK_STREAM")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

    # link the server address with the socket throgh (bind)
    server_socket.bind(SERVER_ADDRESS)

    # the server will keep one user waite if the server busy
    server_socket.listen(3)

    # announce server start for (Debuging)
    print(f"Server listening on {SERVER_ADDRESS} ...")

    # set timer on the "server_socket" because the compiler will blok here "accept()" and we don't want this bloking for long time
    server_socket.settimeout(1.0)
    # to handel any the KeyboardInterrupt inside the loop
    try:
        while True:
            # to handel the timer
            try:
                # make the server wait for clients to connect (bloking)
                connection, address = server_socket.accept()
                # create new thread for the client
                client_thread = threading.Thread(
                    target=handle_client, args=(connection, address), daemon=True
                )
                # start the thread and go back on the loop again to wait another client
                client_thread.start()
            # to check if the time out or not
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print(f"\n[!] Server shutting down properly...")
