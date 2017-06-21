from tkinter import *

class LoginResult():
    def __init__(self):
        self.username = None
        self.server_addr = None
        self.server_port = None
        self.success = False
    def set_username(self, name):
        self.username = name;
    def set_addr(self, addr):
        self.server_addr = addr;
    def set_port(self, port):
        self.server_port = port;
    def set_success(self):
        self.success = True;

def exec_instance(LoginResult):
    loginroot = Tk()
    Label(loginroot, text="Servidor:").grid(row=0,column=0)
    Label(loginroot, text="Porta:").grid(row=1,column=0)
    Label(loginroot, text="Nickname:").grid(row=2,column=0)
    serverEntry = Entry(loginroot)
    portEntry = Entry(loginroot)
    nickEntry = Entry(loginroot)

    serverEntry.grid(row=0,column=1)
    portEntry.grid(row=1,column=1)
    nickEntry.grid(row=2,column=1)

    def loginCommand():
        LoginResult.set_username(str(nickEntry.get()));
        LoginResult.set_addr(str(serverEntry.get()));
        LoginResult.set_port(int(portEntry.get()));
        LoginResult.set_success();
        loginroot.destroy()

    def quit():
        loginroot.destroy()

    quitButton = Button(loginroot,text="Fechar",command=quit)
    quitButton.grid(row=3,column=0)

    loginButton = Button(loginroot,text="Enviar",command=loginCommand)
    loginButton.grid(row=3,column=1)

    loginroot.mainloop()
    
