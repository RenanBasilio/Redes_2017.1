import socket
import ssl
import json
import enum
from threading import Thread

SIZE = 1024

#############################################################################################################################
#
# client_backend.py
# Version: 0.1
# Author: Renan Basilio
# Description: This module describes the logic used to exchange messages between a client and the server (client-side).
#
#############################################################################################################################

class ClientState(enum.Enum):
    READY = 0
    CONNECTED = 1
    STOP = 2

class ClientBackend:
    
    def __init__(self, ip, port, username, color, admin_pass = False):
        self.ip = ip;
        self.port = port;
        self.username = username;
        self.color = color;
        if admin_pass != False:
            self.is_admin = True;
        else:
            self.is_admin = False;
        self.state = ClientState.READY;

    def change_ip(self, ip):
        if self.state != ClientBackend.READY:
            self.ip = ip;
        else:
            print("Failed to change server ip. Connection is open (use close() first!).");

    def change_port(self, port):
        if self.state != ClientBackend.READY:
            self.port = port;
        else:
            print("Failed to change server port. Connection is open (use close() first!).");

    def change_username(self, username):
        self.username = username;
        # Do something

    def change_color(self, color):
        self.color = color;
        # Do something

    def change_addr(self, ip, port):
        change_ip(ip);
        change_port(port);

    def connect(self):
        self.context = ssl.create_default_context();
        self.sock = self.context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname = '127.0.0.1');
        self.sock.connect((self.ip, self.port));
        reg_packet = json.dumps({'type':'NEWUSR', 'uname':self.username, 'color':self.color, 'admin':self.is_admin}).encode('utf-8');
        self.sock.send(reg_packet);
        data = self.sock.recv(SIZE);
        return_packet = json.loads(data.decode('utf-8'));
        if return_packet['type'] == 'OK':
            # Server accepted the connection, now use it.
            self.state = ClientState.CONNECTED;
            self.listen_thread = Thread(None, self.listen, None);
            self.listen_thread.start();
            print("Connected to server.");

    def listen(self):
        try:
            while self.state == ClientState.CONNECTED:
                data = self.sock.recv(SIZE);
                packet = json.loads(data.decode('utf-8'));
                if not packet:
                    print("Connection closed by server.");
                    self.sock.close();
                    self.state = ClientState.READY;
                else:
                    if packet['type'] == 'MSG':
                        print(packet['uname'], ": ", packet['msg']);
        except:
            print("Connection closed by server.")
            self.sock.close();
            self.state = ClientState.READY;

    def send(self, message):
        packet = json.dumps({'type':'MSG', 'uname':self.username, 'color':self.color, 'msg':message}).encode('utf-8')
        self.sock.send(packet);

    def close(self):
        self.sock.shutdown(socket.SHUT_RDWR);
        self.sock.close();
        self.state = ClientState.READY;
        print("Socket closed.")
