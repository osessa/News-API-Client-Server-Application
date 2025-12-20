import socket
import json
from config import  host, port


# Define the menus
main_menu = "1) Search headliens \n2) List of sources \n3) Quit"
search_headliens_menu = "1) Search for keywords \n2) Search by category \n3) Search by Country \n4) List all new headlines \n5) Back to the main menu"

list_of_sources_menu = "1) Search by category \n2) Search by country \n3) Search by language \n4) List all \n5) Back to the main menu"

#Defines the query paremeters
categories_choices = "1) business \n2) general \n3) health \n4) science \n5) sports \n6) technology \n7) Back to menu"

countries_choices = "1) au \n2) ca \n3) jp \n4) ae \n5) sa \n6) kr \n7) us \n8) ma \n9) Back to menu"

languages_choices = "1) ar \n2) en \n3) Back to menu"

#class use to creat socket , connected to server and handle it
class NewsClientServer:
    #constractors run when creat obj to defines main variable needed
    def __init__(self, host=host, port=port):
        self.SERVER_ADDR = (host, port)
        self.client_socket = None

    #function to creat client_socket and connectto the server
    def connect(self):
        #creat socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #connect to server
        self.client_socket.connect(self.SERVER_ADDR)

    #function to close socket
    def close(self):
        if self.client_socket:
            self.client_socket.close()

    #function send json data to server 
    def send_json(self, data: dict):
        payload = json.dumps(data)
        self.client_socket.sendall(payload.encode("utf-8"))
    
    #function recive json data from server 
    def recv_json(self, max_bytes=90000):
        #reciver response
        response = self.client_socket.recv(max_bytes)

        #validate response
        if not response:
            return None
        
        #decode response
        response=response.decode("utf-8")

        #validate response
        if not response:
            return None
        
        #convert response to json
        return json.loads(response.strip())

    #function recive string data from server 
    def recv_text(self, max_bytes=90000):
        #recive data
        response = self.client_socket.recv(max_bytes)
        #ensure it is not empty
        if not response:
            return ""
        #decode data and return it
        return response.decode("utf-8", errors="ignore")

    #function validate if name the user chose avaliable or not
    def validate_name(self):
        #loop until name is validate "avaliable"
        while True:
            #take bane from user
            client_name = input("Please enter your name: ").strip()

            #validate it is not empty
            if not client_name:
                print("Name can not be empty.")
                continue

            #send the chosen name to the server to check it
            self.client_socket.sendall(client_name.encode("utf-8"))

            #recive the chosen name to the server to check it
            response = self.client_socket.recv(1024).decode("utf-8")

            #if server response yes , return vailde name
            if response == "CLIENTNAME_OK":
                return client_name
            else:
                #if server response no then let try agin
                print("Name is taken, Try another.")


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
def get_menu(app: NewsClientServer):

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
            get_headliens_menu(app)
        elif choice == 2:
            get_source_menu(app)
    return


# function to display the search headliens menu for the user to chose from
def get_headliens_menu(app: NewsClientServer):

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
            send_to_server(app, query, "headlines")
        elif choice == 2:
            requst = get_categories_choices()
            if requst is None:
                continue
            query = f"top-headlines?category={requst}"
            send_to_server(app, query, "headlines")
        elif choice == 3:
            requst = get_countries_choices()
            if requst is None:
                continue
            query = f"top-headlines?country={requst}"
            send_to_server(app, query, "headlines")
        elif choice == 4:
            query = "top-headlines?category=general"
            send_to_server(app, query, "headlines")
    return


# function to display the list of sources menu  for the user to chose from
def get_source_menu(app: NewsClientServer):

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
            send_to_server(app, query, "sources")
        elif choice == 2:
            requst = get_countries_choices()
            if requst is None:
                continue
            query = f"sources?country={requst}"
            send_to_server(app, query, "sources")
        elif choice == 3:
            requst = get_language_choices()
            if requst is None:
                continue
            query = f"sources?language={requst}"
            send_to_server(app, query, "sources")
        elif choice == 4:
            query = f"sources"
            send_to_server(app, query, "sources")
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


def send_to_server(app: NewsClientServer, query, type):
    request_dic = {"type": type, "query": query}
    app.send_json(request_dic)

    # receive list as JSON
    list_details = app.recv_json()
    if list_details is None:
        print("No results found.\n")
        return

    list_details_len = len(list_details)
    if list_details_len == 0:
        print("No results found.\n")
        return

    # print list
    count = 1
    for item in list_details:
        # headlines format
        if type == "headlines":
            source = item.get("source", "N/A")
            author = item.get("author", "N/A")
            title = item.get("title", "N/A")
            print(f"{count}\nSource:{source}\nAuthor:{author}\nTitle:{title}\n")
        # sources format
        else:
            name = item.get("name", "N/A")
            print(f"{count}\nSource:{name}\n")
        count += 1

    # ask user to select item
    print(f"Please select itam from 1 to {list_details_len}")
    chosse = read_choice(1, list_details_len)

    # send chosen id
    app.client_socket.sendall(str(chosse).encode("utf-8"))

    # receive details as text
    chosen_details = app.recv_text()
    print(chosen_details + "\n")
    return


if __name__ == "__main__":
    #use class use to creat socket and connected to server
    app = NewsClientServer(host=host, port=port)
    try:
        #try connect to server
        app.connect()

        #take the client name ,validate it ,  send it to server
        app.validate_name()
        
        #display the main menue for user to make requests 
        get_menu(app)
    
    #handel any the KeyboardInterrupt mighthappen inside the try
    except KeyboardInterrupt:
        print(f"\n[!] Client exiting...")

    #handle any erro happen in connection with the server
    except ConnectionResetError:
        print(f"[!] Server disconnected unexpectedly")

    #handle other general errors    
    except Exception as e:
        print(f"[!] An error occurred: {e}")
    #close the socket if user exit    
    finally:
        app.close()
