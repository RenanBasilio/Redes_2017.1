import client_backend

server_connection = client_backend.ClientBackend('127.0.0.1', 9000, 'Test User', 'black')
server_connection.connect();

keepRunning = True;

while keepRunning:
    # Get user input
    user_input = input('');
    if str.upper(user_input) == 'EXIT':
        keepRunning = False;
    else:
        server_connection.send(user_input);

server_connection.close();
