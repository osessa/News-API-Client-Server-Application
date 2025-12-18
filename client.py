import socket

main_menue = "1) Search headliens \n2) List of sources \n3) Quit"
search_headliens_menue = "1) Search for keywords \n2) Search by category \n3) Search by Country \n4) List all new headlines \n5) Back to the main menu"
list_of_sources_menue = "1) Search by category \n2) Search by country \n3) Search by language \n4) List all \n5) Back to the main menu"


def get_menue():
    # while loop take messages from client untill he type "quit"
    while True:
        print("Choose number from 1 to 3:\n")
        print(main_menue)
        message = input("> ")

        if not message.isdigit():
            print("Invalid input")
            continue
        else:
            message = int(message)

        if not message.is_integer() or message > 3 or message < 1:
            print("Invalid input")
            continue

        if message == 3:
            break
        elif message == 1:
            get_headliens_menue()
        elif message == 2:
            get_source_menue()

    return


def get_headliens_menue():
    print("Choose number from 1 to 5:\n")
    print(search_headliens_menue)

    # while loop take messages from client untill he type "quit"
    while True:
        message = input("> ")

        if not message.isdigit():
            print("Invalid input, please choose number from 1 to 5:")
            print(search_headliens_menue)
            continue
        else:
            message = int(message)

        if not message.is_integer() or message > 5 or message < 1:
            print("Invalid input, please choose number from 1 to 5:")
            print(search_headliens_menue)
            continue

        if message == 5:
            break
        elif message == 1:
            print("1")
        elif message == 2:
            print("2")
        elif message == 3:
            print("3")
        elif message == 4:
            print("4")

    return


def get_source_menue():
    print("Choose number from 1 to 5:\n")
    print(list_of_sources_menue)

    # while loop take messages from client untill he type "quit"
    while True:
        message = input("> ")

        if not message.isdigit():
            print("Invalid input, please choose number from 1 to 5:")
            print(list_of_sources_menue)
            continue
        else:
            message = int(message)

        if not message.is_integer() or message > 5 or message < 1:
            print("Invalid input, please choose number from 1 to 5:")
            print(list_of_sources_menue)
            continue

        if message == 5:
            break
        elif message == 1:
            print("1")
        elif message == 2:
            print("2")
        elif message == 3:
            print("3")
        elif message == 4:
            print("4")
    return


# Server IP address and Port number
SERVER_ADDR = ("127.0.0.1", 50555)

# Create client socket ( TCP / IP) and ensure close safely by use 'with'
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

    try:
        # Connect to the server (start the three-way handshake)
        client_socket.connect(SERVER_ADDR)

        # loop to validate the name
        while True:
            # take the name
            client_name = input("Please enter your name: ").strip()
            if not client_name:
                print("Name can not be empty.")
                continue

            client_socket.sendall(client_name.encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8")

            # if name are uniqe then we can take it
            if response == "CLIENTNAME_OK":
                break
            # if the client name are reserved; ask for another name
            else:
                print("Name is taken, Try another.")

        get_menue()

        # # Conver the message to bytes data
        # # Send all the data to the server
        # client_socket.sendall(message.encode("utf-8"))

        # # Receive data from the server
        # # Set maximum data to be reveived at once to 1024 bytes (bloking)
        # data = client_socket.recv(1024)

        # if not data:
        #     print("[-] Server closed the connection.")
        #     break

        # # Convert the bytes data to utf-8 string
        # # Print the received data
        # print("Recevied:", data.decode("utf-8"))

    # Handle errors
    except KeyboardInterrupt:
        print(f"\n[!] Client exiting...")
    except ConnectionResetError:
        print(f"[!] Server disconnected unexpectedly")
    except Exception as e:
        print(f"[!] An error occurred: {e}")
