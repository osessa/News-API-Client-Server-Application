import socket

#Server IP address and Port number
SERVER_ADDR =("127.0.0.1",50555)

#Message to be sent to the Server
message = "Hello TCP"

#Create client socket ( TCP / IP)
client_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

#Connect to the server (start the three-way handshake)
client_socket.connect(SERVER_ADDR)

#Conver the message to bytes data 
#Send all the data to the server
client_socket.sendall(message.encode("ascii"))

#Receive data from the server
#Set maximum data to be reveived at once to 1024 bytes
data = client_socket.recv(1024)

#Convert the bytes data to ASCII string 
#Print the received data
print("Recevied:", data.decode("ascii"))

#Close the client socket
client_socket.close()