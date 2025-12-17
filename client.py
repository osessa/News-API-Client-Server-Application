import socket

# Server IP address and Port number
SERVER_ADDR = ("127.0.0.1", 50555)

# Create client socket ( TCP / IP) and ensure close safely by use 'with'
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

    try:
        # Connect to the server (start the three-way handshake)
        client_socket.connect(SERVER_ADDR)

        print("Connected to the server type message or type (quit) to exit.")

        # while loop take messages from client untill he type "quit"
        while True:
            message = input("> ")

            if message.lower() == "quit":
                break
            # Conver the message to bytes data
            # Send all the data to the server
            client_socket.sendall(message.encode("utf-8"))

            # Receive data from the server
            # Set maximum data to be reveived at once to 1024 bytes (bloking)
            data = client_socket.recv(1024)

            if not data:
                print("[-] Server closed the connection.")
                break

            # Convert the bytes data to ASCII string
            # Print the received data
            print("Recevied:", data.decode("utf-8"))

    # Handle errors
    except ConnectionResetError :
        print(f"[!] Server disconnected unexpectedly")
    except Exception as e:
        print(f"[!] An error occurred: {e}")

