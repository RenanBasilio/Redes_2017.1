from threading import Thread
from threading import Event
from tkinter import *
from tkinter import messagebox
import client_backend

my_username = 'Test User'

server_connection = client_backend.ClientBackend('127.0.0.1', 9000, my_username, 'black')
server_connection.connect();

keepRunning = True;

window = Tk()

scrollbar = Scrollbar(window)
messages = Text(window)
messages.grid(columnspan=19, row=0, column=1, sticky=N+S+E+W)
scrollbar.grid(row=0, column=20, sticky=N+S+W+E)
scrollbar.config(command=messages.yview)
messages.config(yscrollcommand=scrollbar.set)


input_user = StringVar()
input_field = Entry(window, text=input_user)
input_field.grid(sticky=W+E+N+S, row=1, column=1, rowspan=2, columnspan=18, pady=(5, 0))
enter_button = Button(window, text='Send')
enter_button.grid(row=1, column=19, columnspan=2, rowspan=2, sticky=W+E+N+S, pady=(5, 0))

def Enter_pressed(event):
    input_get = input_field.get()
    server_connection.send(input_get)
    messages.insert(INSERT, '{username}: {message}\n'.format(username=my_username, message=input_get))
    input_user.set('')
    return "break"

def Wait_Event(messages):
    while keepRunning:
        if server_connection.message_queue.empty() == False:
            message = server_connection.message_queue.get();
            messages.insert(INSERT, '{username}: {message}\n'.format(username=message['uname'], message=message['msg']))
        else:
            server_connection.message_received_event.wait(100);

frame = Frame(window)  # , width=300, height=300)
input_field.bind("<Return>", Enter_pressed)
messages.bind("<Key>", lambda e: "break")
frame.grid(row=0, column=1)

receive_thread = Thread(None, Wait_Event, None, [messages]);
receive_thread.start();

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        server_connection.close()
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()