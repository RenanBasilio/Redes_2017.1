import client_backend

server_connection = client_backend.ClientBackend('127.0.0.1', 9000, 'Test User', 'black')
server_connection.connect();
server_connection.close();
