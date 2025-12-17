import socket

# Server IP address and Port number
SERVER_ADDR = ("127.0.0.1", 50555)

# Create client socket ( TCP / IP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (start the three-way handshake)
client_socket.connect(SERVER_ADDR)

print("Connected to the server type essage or typr (quit) to exit.")

# while loop take messages from client untill he type "quit"
while True:
    message = input("> ")

    if message.lower() == "quit":
        break
    # Conver the message to bytes data
    # Send all the data to the server
    client_socket.sendall(message.encode("ascii"))

    # Receive data from the server
    # Set maximum data to be reveived at once to 1024 bytes (bloking)
    data = client_socket.recv(1024)

    # Convert the bytes data to ASCII string
    # Print the received data
    print("Recevied:", data.decode("ascii"))

# Close the client socket
client_socket.close()
