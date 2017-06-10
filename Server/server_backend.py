import select
import socket
import ssl
import json

ADDR = ''
PORT = 9000
BACKLOG = 5
SIZE = 1024

#############################################################################################################################
#
# Server Backend
# Version: 1.0
# Author: Renan Basilio
# Description: This module describes the method that runs in the background of our server.
# Arguments:
#     wait_for_interface : Whether this backend should wait for an interface socket to connect before serving other clients.
#     interface_pass : Code to be used for authenticating the server interface.
#
#############################################################################################################################

def server_backend(wait_for_interface = False, interface_pass = None):
    # Initialize SSL Context
    server_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH);
    server_context.load_cert_chain(certfile="cert_chatRedes.pem", keyfile="key_chatRedes.pem")
    server_context.check_hostname = False

    # Initialize Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

    server_socket.bind((ADDR, PORT));
    server_socket.listen(BACKLOG);

    keepRunning = True;

    # Declare socket to use for interface
    interface_socket = None;

    # If an interface is expected, loop until one succesfully authenticates
    while wait_for_interface:
        client, address = server_socket.accept();
        # If address matches local address
        if address[0] == '127.0.0.1':
            # Wrap socket in secure layer
            ssl_client = server_context.wrap_socket(client, server_side=True)  # This socket is local and doesnt really need to be secure, but it's good reference for programming the client
            # Read data from socket. First packet should be an authentication packet
            data = ssl_client.recv(SIZE);
            # Decode packet to json and load it
            message = json.loads(data.decode('utf-8'));
            # If user and password match agreed values, register socket as interface socket and exit loop
            if message['user'] == 'server_interface' and message['password'] == interface_pass:
                interface_socket = ssl_client;
                wait_for_interface = False;
            # Otherwise close the connection, it's not the one we're waiting for
            else:
                ssl_client.close();
        # Otherwise close the connection, it's not the one we're waiting for
        else:
            client.close();

    # Register the server socket into input sources
    input_sources = [server_socket]

    # If using an interface socket, register it as well
    if interface_socket != None:
        input_sources.append(interface_socket);

    while keepRunning:
        
        # Select to block until socket activity
        inputready, outputready, exceptready = select.select(input_sources, [], [])
        
        # For each active socket
        for s in inputready:

            if s == server_socket:
                # Handle incoming connections
                client, address = server.accept()
                input.append(client)

            elif s == interface_socket:
                # Handle server interface commands
                data = s.recv(SIZE)
                message = json.loads(data.decode('utf-8'));
                if message['cmd'] == 'exit':
                    # This command exits the server
                    response = json.dumps({'rsp':'EXIT', 'str':'Server shutting down...'}).encode('utf-8');
                    keepRunning = False;
                else:
                    response = json.dumps({'rsp':'UNREC_CMD', 'str':'ERROR: Command not recognized.'}).encode('utf-8');
                s.send(response);
            else:
                # Handle client socket activity
                data = s.recv(SIZE)
                if data:
                    message = json.loads(data.decode('utf-8'));
                else:
                    s.close()
                    input_sources.remove(s)

    # Close open sockets in input sources
    for s in input_sources:
        s.close();
