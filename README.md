# News API Client-Server Application

## Project Description
This project is a **Client–Server application** that uses **TCP** and developed using **Python**.  
The system allows multiple clients to connect to a server and retrieve news data from the **NewsAPI** service.

The server is able to handle multiple clients at the same time using **threading**, fetches data from the NewsAPI, and sends structured JSON responses back to the clients.  
Each client request is also **logged and saved into a JSON file** for testing and evaluation purposes.

The client provides an interactive **menu-driven interface** to the user that allows them to:
- Search news headlines
- Filter news by category, country, or keyword
- List available news sources
- View detailed information about selected articles or sources

---

## Semester
First Semester – Academic Year 2025/2026

---

## Group Information
- **Group Name:** GB7  
- **Course Code:** ITNE352 – Network Programming  
- **Section:** 2  
- **Student Name:** Osama essa , Sara Ismail  
- **Student ID:** *202305787* , *202306311*

---

## Table of contents:
1. [Requirements](#requirements)
2. [How to Run the System](#how-to-run-the-system)
3. [Scripts](#scripts)
4. [Additional Concepts](#additional-concepts)
5. [Acknowledgments](#acknowledgments)
6. [Conclusion](#conclusion)
7. [Resources](#resources-optional)

## Requirements
To run this project in your local host, make sure you have the following installed:

### Software Requirements
- Python **3.9 or higher**
- Internet connection for NewsAPI request

### Python Libraries
Install the required dependencies using:
```bash
pip install requests

## How to Run the System
1. open `config.py`
 put your:
   - Host address
   - NewsAPI key
   - Group ID


2. Run the server 
 - open the terminal
 - write `python server.py`

3.  Run the client 
 - open the terminal
 - write `python client.py`

4. Intract with the server
 -enter your name
 -Choose options from the menu
 -Select articles or sources to view more details about it
 -you can see each request will be saved automatically in a JSON file named : <client_name>_<request_type>_<group_id>.json


---

## Scripts

1. **Server Scripts:**
   Main Responsibilities:
      -Accept connections request from multiple clients through TCP sockets
      -Handle each client connection in a separate thread
      -Fetch data from NewsAPI
      -Send JSON responses to clients
      -Save API responses in JSON files for evaluation
   Libraries Used:
      -socket
      -threading
      -requests
      -json
      -os

2. **Client Scripts:**
   Main Responsibilities:
      -Connect to the server through TCP socket
      -Display interactive menus to the user
      -Send user requests in JSON format to the server
      -Receive and display server responses
   Features:
      -Menu-based navigation
      -Input validation
      -Detailed viewing for the selected item
   Libraries Used:
      -socket
      -json


3. **Configuration Script**
   Main Responsibilities:
      -Store all system configuration values: NewsAPI key,Server host and port , Group Id
   Features:
      -Allow easy configuration to run the application without modifying the main application scripts
 

---

## Additional concept
Object-Oriented-Programming (OOP)
-Server and client logic structured using classes
-Encapsulation networking and API logic in one place
-Clear separation of responsibilities
-Avoid repetition on the code

## Acknowledgments 
It was vary useful to work in this project from  scratch and learning network programming concept under Dr. Mohd Almeer instruction and support and we extend our sincere thanks to him To teach us this course "ITNE352"
   
## Conclusion
In Conclusion This project demonstrates the implementation of:
   -TCP socket programming
   -Multithreading
   -API integration
   -Object-Oriented Programming
   -JSON-based data storage

The system provides a complete and functional client–server Application for interactive with API and receive responses as real-world network programming scenarios.

## Resources
1.https://newsapi.org/
2.https://docs.python.org/3/
3.https://docs.python-requests.org/
