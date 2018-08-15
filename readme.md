# CS410-510-Agile

Pre-Requisites
1.  Python2.7 (Not Python3)
2.  prettytable
- pip install prettytable
- or
- pip install https://pypi.python.org/packages/source/P/PrettyTable/prettytable-0.7.2.tar.bz2
- You may want to sudo while installing this package since it gave a a lot of pain with permissions during installion

Run server in command line: python server.py
Run client in command line: python client.py username password

Run the server first, then other clients can connect. Right now the default host ip is local host (127.0.0.1)
Server will continue to run forever while clients connect. 

When server first connects it will make Serverlocation directory on current working directory of server.
When clients connect, a Clientlocation directory will be made on current working directory of client.
These two directories are the primary means of transfer between files.

When client successfully connects, will be prompted with choosing a command. Use help command to display all possible commands.
Clients can continue to issue commands untill desired or client connection ends with server. 

NOTE: This project is built on Unix and has not been tested on Windows.
