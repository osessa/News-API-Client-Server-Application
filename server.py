import socket
import threading
import requests
import json
from config import NEWS_API_KEY

# set to keep records of the active client names
active_clients = set()
# use lock to ensere the thread safety
lock = threading.Lock()


def list_details_headlines(url, query_type):
    response = requests.get(url)
    json_result = response.json()
    articales = json_result.get("articles", [])
    output = []
    num_of_articales = 1
    for articale in articales[:15]:
        source = articale.get("source", {}).get("name", "N/A")
        author = articale.get("author", "N/A")
        title = articale.get("title", "N/A")

        output.append(
            f"{num_of_articales}\nSource:{source}\nAuthor:{author}\nTitle:{title}\n"
        )
        num_of_articales += 1
    
    if not output:
        output.append("No results found.")
    connection.sendall("\n".join(output).encode("utf-8"))

def list_details_sources(url, query_type):
    response = requests.get(url)
    json_result = response.json()
    sources = json_result.get("sources", [])
    output = []
    num_of_sources = 1
    for source in sources[:15]:
        source = source.get("name", "N/A")
       
        output.append(
            f"{num_of_sources}\nSource:{source}\n"
        )
        num_of_sources += 1
    
    if not output:
        output.append("No results found.")
    connection.sendall("\n".join(output).encode("utf-8"))

# handle the client thread function
def handle_client(connection, address):
    client_name = None
    try:
        # auto close connection by use 'with'
        with connection:
            # <----------- Validate name loop ------------>
            while True:
                # reserve client name
                client_name = connection.recv(1024).decode("utf-8").strip()

                with lock:
                    # check if client name are reserve in the set or not
                    if client_name in active_clients:
                        connection.sendall("CLIENTNAME_TAKEN".encode("utf-8"))
                        continue
                    # if not reserved
                    else:
                        active_clients.add(client_name)
                        connection.sendall("CLIENTNAME_OK".encode("utf-8"))
                        # announce new client connection
                        print(f"[+] New client connected [{client_name}]")
                        break

            # <----------- Messages loop ------------>
            while True:
                # recive data from client
                client_request_dic = connection.recv(1024).decode("utf-8").strip()
                client_request_dic=json.loads(client_request_dic)
                # extract data
                client_query = client_request_dic["query"]
                client_query_type = client_request_dic["type"]

                if not client_query:
                    break

                if "?" in client_query:
                    url = f"https://newsapi.org/v2/{client_query}&apiKey={NEWS_API_KEY}"
                else:
                    url = f"https://newsapi.org/v2/{client_query}?apiKey={NEWS_API_KEY}"

                if client_query_type=="headlines":
                    list_details_headlines(url,client_query_type)
                elif client_query_type=="sources":
                    list_details_sources(url, client_query_type)

    except ConnectionResetError:
        if client_name:
            print(f"[!] Client [{client_name}] disconnected unexpectedly")
        # if client did not have name yet then use there address.
        else:
            print(f"[!] Client [{address}] disconnected unexpectedly")

    except Exception as e:
        if client_name:
            print(f"[!] Error with Client [{client_name}]: {e}")
        # if client did not have name yet then use there address.
        else:
            print(f"[!] Error with Client [{address}]: {e}")

    finally:
        with lock:
            active_clients.discard(client_name)
            # announce client disconnection
            if client_name:
                print(f"[-] Client disconnected [{client_name}]")

            # if client did not have name yet then use there address.
            else:
                print(f"[-] Client disconnected [{address}]")


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
