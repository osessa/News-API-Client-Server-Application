import socket
import json
# Define the menus
main_menu = "1) Search headliens \n2) List of sources \n3) Quit"
search_headliens_menu = "1) Search for keywords \n2) Search by category \n3) Search by Country \n4) List all new headlines \n5) Back to the main menu"
list_of_sources_menu = "1) Search by category \n2) Search by country \n3) Search by language \n4) List all \n5) Back to the main menu"
categories_choices = "1) business \n2) general \n3) health \n4) science \n5) sports \n6) technology \n7) Back to menu"
countries_choices = (
    "1) au \n2) ca \n3) jp \n4) ae \n5) sa \n6) kr \n7) us \n8) ma \n9) Back to menu"
)
languages_choices = "1) ar \n2) en \n3) Back to menu"


# Validate the user choice function
def read_choice(min_val, max_val):
    while True:
        # read user input
        choice = input("> ")

        # check if the input is digit, ask again if not
        if not choice.isdigit():
            print(f"Invalid input, choose number {min_val} to {max_val}")
            continue

        choice = int(choice)

        # check if the input in the range, ask again if not
        if choice < min_val or choice > max_val:
            print(f"Invalid input, choose number {min_val} to {max_val}")
            continue

        # return choice if it pass all checks
        return choice


# function to display the main menu for the user to chose from
def get_menu():

    # loop to take user choice until he choices 3 to exit
    while True:
        # display the menu
        print("Choose number from 1 to 3:")
        print(main_menu)

        # read and vailidate user choice
        choice = read_choice(1, 3)
        # handle user choice
        if choice == 3:
            break
        elif choice == 1:
            get_headliens_menu()
        elif choice == 2:
            get_source_menu()
    return


# function to display the search headliens menu for the user to chose from
def get_headliens_menu():

    # loop to take user choice until he choices 5 to return to main menu
    while True:
        # display the  menu
        print("Choose number from 1 to 5:")
        print(search_headliens_menu)
        # read and vailidate user choice
        choice = read_choice(1, 5)

        # handle user choice
        if choice == 5:
            break
        elif choice == 1:
            requst = input("write the key word: ").strip()
            if not requst:
                continue
            query = f"top-headlines?q={requst}"
            send_to_server(query,"headlines")
        elif choice == 2:
            requst = get_categories_choices()
            if requst is None:
                continue
            query = f"top-headlines?category={requst}"
            send_to_server(query,"headlines")
        elif choice == 3:
            requst = get_countries_choices()
            if requst is None:
                continue
            query = f"top-headlines?country={requst}"
            send_to_server(query,"headlines")
        elif choice == 4:
            query = "top-headlines?category=general"
            send_to_server(query,"headlines")
    return


# function to display the list of sources menu  for the user to chose from
def get_source_menu():

    # loop to take user choice until he choices 5 to return to main menu
    while True:
        print("Choose number from 1 to 5:")
        print(list_of_sources_menu)
        # read and vailidate user choice
        choice = read_choice(1, 5)

        # handle user choice
        if choice == 5:
            break
        elif choice == 1:
            requst = get_categories_choices()
            if requst is None:
                continue
            query = f"sources?category={requst}"
            send_to_server(query,"sources")
        elif choice == 2:
            requst = get_countries_choices()
            if requst is None:
                continue
            query = f"sources?country={requst}"
            send_to_server(query,"sources")
        elif choice == 3:
            requst = get_language_choices()
            if requst is None:
                continue
            query = f"sources?language={requst}"
            send_to_server(query,"sources")
        elif choice == 4:
            query = f"sources"
            send_to_server(query,"sources")
    return


# function to display the list of categories choices for the user to chose from
def get_categories_choices():

    # loop to take user choice until he choices 7 to return back to menu
    while True:
        print("Choose number from 1 to 7:")
        print(categories_choices)
        # read and vailidate user choice
        choice = read_choice(1, 7)

        # handle user choice
        if choice == 1:
            return "business"
        elif choice == 2:
            return "general"
        elif choice == 3:
            return "health"
        elif choice == 4:
            return "science"
        elif choice == 5:
            return "sports"
        elif choice == 6:
            return "technology"
        elif choice == 7:
            break
    return


# function to display the list of languages choices for the user to chose from
def get_language_choices():

    # loop to take user choice until he choices 3 to return back to menu
    while True:
        print("Choose number from 1 to 3:")
        print(languages_choices)
        # read and vailidate user choice
        choice = read_choice(1, 3)

        # handle user choice
        if choice == 1:
            return "ar"
        elif choice == 2:
            return "en"
        elif choice == 3:
            break
    return


# function to display the list of countries choices for the user to chose from
def get_countries_choices():

    # loop to take user choice until he choices 9 to return back to menu
    while True:
        print("Choose number from 1 to 9:")
        print(countries_choices)
        # read and vailidate user choice
        choice = read_choice(1, 9)

        # handle user choice
        if choice == 1:
            return "au"
        elif choice == 2:
            return "ca"
        elif choice == 3:
            return "jp"
        elif choice == 4:
            return "ae"
        elif choice == 5:
            return "sa"
        elif choice == 6:
            return "kr"
        elif choice == 7:
            return "us"
        elif choice == 8:
            return "ma"
        elif choice == 9:
            break
    return


def send_to_server(query,type):
    request_dic = {"type": type , "query":query}
    payLoad = json.dumps(request_dic)
    client_socket.sendall(payLoad.encode("utf-8"))

    response = client_socket.recv(90000)

    if not response:
        print("No results found.\n")
        return

    list_details = response.decode("utf-8").strip()

    if not list_details:
        print("No results found.\n")
        return

    list_details = json.loads(list_details)
 
    list_details_len = len(list_details)

    
    count=1
    for articale in list_details:
        source = articale.get("source", "N/A")
        author = articale.get("author", "N/A")
        title  = articale.get("title", "N/A")

        print(f"{count}\nSource:{source}\nAuthor:{author}\nTitle:{title}\n")
        count += 1
    
    if count==0:
        print("No results found.\n")
        return
    #ask user to select iteam for more details and validate thier choose
    print(f"Please select itam from 1 to {list_details_len}")
    chosse = read_choice(1,list_details_len)
    
    #send id of choosen iteam
    client_socket.sendall(str(chosse).encode("utf-8"))

    #recive 'string' details about choosen iteam and print it
    chosen_articale_details = client_socket.recv(90000).decode("utf-8")
    print(chosen_articale_details+'\n')

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

        get_menu()

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
