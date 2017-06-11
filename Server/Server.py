from threading import Thread
import socket
import ssl
import json
import server_backend as backend


#############################################################################################################################
#
# Server.py
# Version: 1.0
# Author: Renan Basilio
# Description: This module describes initialization and interface tasks for the chat server.
#
#############################################################################################################################

interface_passkey = 1111;   # This is the passkey to authenticate the interface connection to the backend. Make random number later.

# Initialize server backend thread
print("Initializing server...");
server_thread = Thread(None, backend.server_backend, None, [True, interface_passkey]);

# Start the server
server_thread.start();
print("Server thread started.");

# Create SSL context for interface connection to server
print("Connecting interface to server...");
context = ssl.create_default_context();

# Create and wrap interface socket
interface_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname = '127.0.0.1');

# Connect to server
interface_socket.connect(('127.0.0.1', backend.PORT));

# Create connection packet with appropriate user and passkey
auth_packet = json.dumps({'user':'server_interface', 'password':interface_passkey}).encode('utf-8');

# Send auth packet to server backend
interface_socket.send(auth_packet);

print("Server interface connected. Awaiting input.")

keepRunning = True;

# While the program should continue to run
while keepRunning:
    # Get user input
    server_input = input('> ');
    # Generate interface command packet with user input and send to server
    packet = json.dumps({'cmd':str.upper(server_input)}).encode('utf-8');
    interface_socket.send(packet);
    # Receive and print response from server
    data = interface_socket.recv(backend.SIZE);
    message = json.loads(data.decode('utf-8'));
    print(message['str']);
    
    # If command to exit was received, shut down
    if message['rsp'] == 'EXIT':
        keepRunning = False;

server_thread.join();
print("Server closed successfully.");