import socket
import threading
import requests
import json
from config import NEWS_API_KEY, host, port, group_id, BASE_URL
import os


# class handle keeping requests history in jison file
class RequestLogger:
    # constractors run when creat obj to defines main variable needed
    def __init__(self, group_id: str):
        # store group id as string
        self.group_id = group_id

    # function that add record to jison file
    def add_record(self, client_name, client_query_type, response):
        # formate jison file name to contain :client_name,client_query_type, group_id
        file_name = f"{client_name}_{client_query_type}_{self.group_id}.json"

        # list of data to save data went write it on the file
        existing_data = []

        # if the file exist we reaad existing data and save them list of data
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as file:
                try:
                    existing_data = json.load(file)
                # to catch any erro in reading the file
                except json.JSONDecodeError:
                    existing_data = []

        # ensure type of data
        if not isinstance(existing_data, list):
            existing_data = [existing_data]

        # add the resonse to the list of data
        existing_data.append(response)

        # write the list of data on the file
        with open(file_name, "w", encoding="utf-8") as file:
            # write the data as jison format
            json.dump(existing_data, file, indent=4, ensure_ascii=False)


# class handle send request to NewsAPI and recive response
class NewsAPIFetcher:
    # function to build the correct url based on client parmeters
    def build_url(self, client_query: str):
        if "?" in client_query:
            return f"{BASE_URL}{client_query}&apiKey={NEWS_API_KEY}"
        else:
            return f"{BASE_URL}{client_query}?apiKey={NEWS_API_KEY}"

    # function to send the request to NewsAPI to get the response
    def fetch(self, client_query):
        # use build_url() to build the correct url based on client parmeters
        url = self.build_url(client_query)
        # send the request for NewsAPI to get the response
        response = requests.get(url)
        # convert the response to json and send it
        return response.json()


# class to start a server and handle connection to it
class NewsServer:
    # constractors run when creat obj to defines main variable needed
    def __init__(self, group_id=group_id):
        #           (IP + Port Number)
        self.SERVER_ADDRESS = (host, port)

        # use lock to ensere the thread safety
        self.lock = threading.Lock()

        # set to keep records of the active client names
        self.active_clients = set()

        # looger to keep record of response everytime we make request and recive response
        self.logger = RequestLogger(group_id)

        # use to make any request to NewsAPI
        self.api = NewsAPIFetcher()

    # function recive client name, vaildate client name and return vaild name
    def validate_client_name(self, connection):
        # <----------- Validate name loop ------------>
        # loop until client enter valid name
        while True:
            # reserve client name
            client_name = connection.recv(1024).decode("utf-8").strip()

            with self.lock:
                # check if client name are reserve in the set or not
                if client_name in self.active_clients:
                    # send not vaild to try agin
                    connection.sendall("CLIENTNAME_TAKEN".encode("utf-8"))
                    continue
                # if not reserved
                else:
                    # add client name to set of clients name
                    self.active_clients.add(client_name)
                    # send vaildation
                    connection.sendall("CLIENTNAME_OK".encode("utf-8"))
                    # announce new client connection erver screen
                    print(f"[+] New client connected [{client_name}]")
                    # retrun the vaild name
                    return client_name

    # function send  response to the client and let them select iteam for more details for headlines query type
    def send_headlines_list(self, connection, api_response):
        # extract the rsult from api_response
        articales = api_response.get("articles", [])

        # list to save only first 15 result
        results = []

        # counter for validate num of result "if there is any result"
        count = 0

        # loop in  first 15 articales ans save it in formatted way
        for i, article in enumerate(articales[:15], start=1):
            count += 1
            results.append(
                {
                    "id": i,
                    "source": article.get("source", {}).get("name", "N/A"),
                    "author": article.get("author", "N/A"),
                    "title": article.get("title", "N/A"),
                }
            )

        # send result to client
        connection.sendall(json.dumps(results).encode("utf-8"))

        # validate num of result , if there is no result no nned to continue
        if count == 0:
            return

        # reciver the id of selected articale for more details
        chosen_articale_id = int(connection.recv(1024).decode("utf-8").strip())

        # extract chosen artical
        chosen_articale = articales[chosen_articale_id - 1]

        # formate details about chosen artical
        details = (
            f"Source name : {chosen_articale.get('source', {}).get('name', 'N/A')}\n"
            f"Author: {chosen_articale.get('author', 'N/A')}\n"
            f"Title: {chosen_articale.get('title', 'N/A')}\n"
            f"Description: {chosen_articale.get('description', 'N/A')}\n"
            f"URL: {chosen_articale.get('url', 'N/A')}\n"
            f"Published Date & Time: {chosen_articale.get('publishedAt', 'N/A')}\n"
        )
        # send details about chosen artical to client
        connection.sendall(details.encode("utf-8"))

    # function send  response to the client and let them select iteam for more details for sources query type
    def send_sources_list(self, connection, api_response):
        # extract the rsult from api_response
        sources = api_response.get("sources", [])

        # list to save only first 15 result
        results = []

        # counter for validate num of result "if there is any result"
        count = 0

        # loop in  first 15 articales ans save it in formatted way
        for i, source in enumerate(sources[:15], start=1):
            count += 1
            results.append({"id": i, "name": source.get("name", "N/A")})

        # send result to client
        connection.sendall(json.dumps(results).encode("utf-8"))

        # validate num of result , if there is no result no nned to continue
        if count == 0:
            return

        # reciver the id of selected articale for more details
        chosen_id = int(connection.recv(1024).decode("utf-8").strip())

        # extract chosen result
        chosen = sources[chosen_id - 1]

        # formate details about chosen artical
        details = (
            f"Source name : {chosen.get('name', 'N/A')}\n"
            f"Description: {chosen.get('description', 'N/A')}\n"
            f"URL: {chosen.get('url', 'N/A')}\n"
            f"Country: {chosen.get('country', 'N/A')}\n"
            f"Language: {chosen.get('language', 'N/A')}\n"
            f"Category: {chosen.get('category', 'N/A')}\n"
        )
        # send details about chosen artical to client
        connection.sendall(details.encode("utf-8"))

    # function to handle client connection
    def handle_client(self, connection, client_address):
        client_name = None
        try:
            # auto close connection by use 'with'
            with connection:
                # use function to take client name and validate it
                client_name = self.validate_client_name(connection)

                # <----------- Messages loop ------------>
                while True:
                    # recive request from client
                    client_request_dic = connection.recv(1024)

                    # validate request
                    if not client_request_dic:
                        break

                    # decode request
                    client_request_dic = client_request_dic.decode("utf-8").strip()

                    # validate request
                    if not client_request_dic:
                        break

                    # convert data to json
                    client_request_dic = json.loads(client_request_dic)

                    # extract request query and query type
                    client_query = client_request_dic["query"]
                    client_query_type = client_request_dic["type"]

                    # validate request
                    if not client_query:
                        break

                    # send request to api and get the response
                    api_response = self.api.fetch(client_query)

                    # print request details in server screen
                    print(
                        f"[{client_name}] request type: {client_query_type}, request parameter: {client_query}."
                    )

                    # send the response to the client and le them select iteam for more details based on the query type
                    if client_query_type == "headlines":
                        self.send_headlines_list(connection, api_response)
                    elif client_query_type == "sources":
                        self.send_sources_list(connection, api_response)

                    # add api response to json file to keep records
                    self.logger.add_record(client_name, client_query_type, api_response)

        # handle erro with client connection
        except ConnectionResetError:
            if client_name:
                # print an announce on server screen
                print(f"[!] Client [{client_name}] disconnected unexpectedly")

            # if client did not have name yet then use there address in the announce
            else:
                print(f"[!] Client [{client_address}] disconnected unexpectedly")

        # handle other general errors
        except Exception as e:
            if client_name:
                # print an announce on server screen
                print(f"[!] Error with Client [{client_name}]: {e}")
            # if client did not have name yet then use there address.
            else:
                print(f"[!] Error with Client [{client_address}]: {e}")

        # if vlient exsit
        finally:
            with self.lock:
                if client_name:
                    # remove client name from set of active client
                    self.active_clients.discard(client_name)
                    # print an announce on server screen
                    print(f"[-] Client disconnected [{client_name}]")
                # if client did not have name yet then use there address.
                else:
                    print(f"[-] Client disconnected [{client_address}]")

    # function make server socket and accept the clients
    def start(self):
        # create the socket and this socket have ("AF_INET": Address Family Internet = IPv4, TCP "SOCK_STREAM")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

            # link the server address with the socket throgh (bind)
            server_socket.bind(self.SERVER_ADDRESS)

            # the server will keep one user waite if the server busy
            server_socket.listen(3)

            # set timer on the "server_socket" because the compiler will blok here "accept()" and we don't want this bloking for long time
            server_socket.settimeout(1.0)

            # announce server start (for Debuging)
            print(f"Server listening on {self.SERVER_ADDRESS} ...")

            try:
                while True:
                    # use try to handel the timer inside it
                    try:
                        # make the server wait for clients to connect (bloking)
                        connection, client_address = server_socket.accept()

                        # create new thread for the client
                        client_thread = threading.Thread(
                            target=self.handle_client,
                            args=(connection, client_address),
                            daemon=True,
                        )

                        # start the thread and go back on the loop again to wait another client
                        client_thread.start()

                    # to check if the time out or not
                    except socket.timeout:
                        continue

            # handel any the KeyboardInterrupt mighthappen inside the loop
            except KeyboardInterrupt:
                print(f"\n[!] Server shutting down properly...")


if __name__ == "__main__":
    NewsServer(group_id=group_id).start()
