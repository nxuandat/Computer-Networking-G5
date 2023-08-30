import socket
from threading import Thread
from tkinter import Tk, W, E
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from PIL import Image
import Keystroke_Client
import processRunning_Client
import appRunning_Client
import screenCapture_Client


class Main:
    def __init__(self):
        self.Home = Tk()
        self.Home.withdraw()
        self.Home.configure(bg="#fff")

        self.login = Toplevel()
        self.login.configure(bg="#fff")
        self.login.title("Login")
        self.login.geometry("650x650")
        self.login.iconbitmap('./img/button/remoteIcon.ico')
        self.login.resizable(False, False)
        self.background = PhotoImage(file='./img/button/background.png')
        self.mylabel = Label(self.login, image=self.background)
        self.mylabel.place(x=0, y=0, relwidth=1, relheight=1)
        self.labelIP = Label(self.login, text="Nhập địa chỉ IP để tiếp tục:",
                             compound="center", bg="#fff", font="Helvetica 15 bold")
        self.labelIP.place(relx=0.05, rely=0.05)
        SERVER_IP = socket.gethostbyname(socket.gethostname())
        print(SERVER_IP)

        self.input_IP = Entry(self.login, bg="#fff", font="Helvetica 14")
        self.input_IP.insert(END, SERVER_IP)
        self.input_IP.place(relx=0.501, rely=0.05)
        self.input_IP.focus()
        connectButton = PhotoImage(file='./img/button/connect.png')
        self.connect = Button(self.login, image=connectButton, bg="#fff", font="Helvetica 15 bold", command=(
            lambda: self.Connection_handling(self.input_IP.get())), activebackground="#f7f7f7", relief="flat", bd=0, highlightthickness=0)

        self.connect.pack(pady=120, padx=20, anchor="center")
        self.Home.mainloop()

    def Controller(self, Client):
        self.btnProcess = PhotoImage(
            file='./img/button/processRunning.png')
        self.process = Button(self.login, image=self.btnProcess, command=(
            lambda: self.process_function(Client)), bg="#fff", relief="flat", bd=0, highlightthickness=0)
        self.process.place(relx=0.05, rely=0.4)
        self.btnApp = PhotoImage(file='./img/button/appRunning.png')
        self.app = Button(self.login, image=self.btnApp, command=(
            lambda: self.application_function(Client)), bg="#fff", relief="flat", bd=0, highlightthickness=0)
        self.app.place(relx=0.240, rely=0.4)
        self.btnSCapture = PhotoImage(
            file='./img/button/screenCapture.png')
        self.capture = Button(self.login,  image=self.btnSCapture, command=(
            lambda: self.screenCapture(Client)), bg="#fff", relief="flat", bd=0, highlightthickness=0)
        self.capture.place(relx=0.240, rely=0.758)
        self.btnKStroke = PhotoImage(
            file='./img/button/keyStroke.png')
        self.key = Button(self.login, image=self.btnKStroke, command=(
            lambda: self.keyStroke(Client)), bg="#fff", relief="flat", bd=0, highlightthickness=0)
        self.key.place(relx=0.765, rely=0.4)
        self.btnSDwon = PhotoImage(file='./img/button/shutDown.png')
        self.shut = Button(self.login, image=self.btnSDwon, command=(
            lambda: self.shutDown(Client)), bg="#fff", relief="flat", bd=0, highlightthickness=0)
        self.shut.place(relx=0.245, rely=0.58)
        self.btnExist = PhotoImage(file='./img/button/exit.png')
        self.escape = Button(self.login, image=self.btnExist, command=(
            lambda: self.Exit(Client)), bg="#fff", relief="flat", bd=0, highlightthickness=0)
        self.escape.place(relx=0.505, rely=0.58)

    def screenCapture(self, Client):
        try:
            screenCapture_Client.screencapture(Client)
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối")

    def application_function(self, Client):
        try:
            appRunning_Client.apprunning(Client)
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")

    def process_function(self, Client):
        try:
            processRunning_Client.processrunning(
                Client)
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")

    def keyStroke(self, Client):
        try:
            Keystroke_Client.keystroke(Client)
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")

    def shutDown(self, Client):
        try:
            Client.send(bytes("Shutdown", 'utf-8'))
            messagebox.showinfo("Success", "Máy tính sẽ tắt sau 40s")
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")

    def Exit(self, Client):
        try:
            Client.send(bytes("Exit", 'utf-8'))
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")
        Client.close()
        self.Home.destroy()

    def Connection_handling(self, HOST):
        PORT = 3000
        Client = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        try:
            Client.connect((HOST, PORT))
            messagebox.showinfo("Successful !!!", "Kết nối server thành công")
            rcv = Thread(target=self.Controller(Client))
            rcv.start()
        except:
            messagebox.showinfo(" Error!!!", "Không thể kết nối đến server")
            Client.close()


if __name__ == "__main__":
    Main()
