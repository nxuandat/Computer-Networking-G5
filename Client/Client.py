import socket       # thư viện socket
from threading import Thread
from tkinter import Tk, W, E
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import ttk
from tkinter import *  # Thư viện GUI
from tkinter import messagebox
from PIL import ImageTk, Image
from PIL import Image
import Keystroke_Client				# KeyStroke.py
import processRunning_Client 		# process_function.py
import appRunning_Client			# application_function.py
import screenCapture_Client 			# screenCapture.py

# AF_INET        : cho biết đang yêu cầu một socket Internet Protocol(IP), cụ thể là IPv4
# SOCK_STREAM    : chỉ loại kết nối TCP IP hoặc UDP . Chương trình nhóm em sẽ chạy trên một cổng kết nối TCP
# bind()         : Phương thức này gắn kết địa chỉ (host,port) tới Socket
# listen()       : Phương thức này cho phép một cái chờ kết nối từ một các client.
# accept()       : Phương thức này chấp nhận một cách thụ động kết nối TCP Client, đợi cho tới khi kết nối tới.
# recv()         : Phương thức này nhận TCP message.
# send()         : Phương thức này gửi TCP message.
# close()        : Phương thức này đóng kết nối.
# gethostbyname(): Trả về hostname.


class Main:
    def __init__(self):
        self.Home = Tk()
        self.Home.withdraw()
        self.Home.configure(bg="#fff")

    # Hộp thoại đăng nhập IP
        self.login = Toplevel()
        self.login.configure(bg="#fff")
    # Tạo tiêu đề cho hộp thoại
        self.login.title("Login")
        self.login.geometry("650x650")
        self.login.iconbitmap('./img/button/remoteIcon.ico')
        self.login.resizable(False, False)
        self.background = PhotoImage(file='./img/button/background.png')
        self.mylabel = Label(self.login, image=self.background)
        self.mylabel.place(x=0, y=0, relwidth=1, relheight=1)
    # Tạo label
        self.labelIP = Label(self.login, text="Nhập địa chỉ IP để tiếp tục:",
                             compound="center", bg="#fff", font="Helvetica 15 bold")
        self.labelIP.place(relx=0.05, rely=0.05)
    # Tạo input text IP
        SERVER_IP = socket.gethostbyname(socket.gethostname())
        print(SERVER_IP)

        self.input_IP = Entry(self.login, bg="#fff", font="Helvetica 14")
        self.input_IP.insert(END, SERVER_IP)
        self.input_IP.place(relx=0.501, rely=0.05)
        self.input_IP.focus()  # tạo con trỏ nhấp nháy trong ô text
    # Tạo nút nhấn, khi nhấn nút =>  dữ liệu sẽ được gửi đến server thông qua socket
        connectButton = PhotoImage(file='./img/button/connect.png')
        self.connect = Button(self.login, image=connectButton, bg="#fff", font="Helvetica 15 bold", command=(
            lambda: self.Connection_handling(self.input_IP.get())), activebackground="#f7f7f7", relief="flat", bd=0, highlightthickness=0)

        # Toạ độ y và x của nút kết nối
        self.connect.pack(pady=120, padx=20, anchor="center")
        self.Home.mainloop()							# Chạy hệ thống

    def Controller(self, Client):  # Hộp thoại các chức năng điều khiển
        # Process Running
        self.btnProcess = PhotoImage(
            file='./img/button/processRunning.png')                      # Đặt hình ảnh
        self.process = Button(self.login, image=self.btnProcess, command=(
            lambda: self.process_function(Client)), bg="#fff", relief="flat", bd=0, highlightthickness=0)
        self.process.place(relx=0.05, rely=0.4)
    # App Running
        # Đặt hình ảnh
        self.btnApp = PhotoImage(file='./img/button/appRunning.png')
        self.app = Button(self.login, image=self.btnApp, command=(
            lambda: self.application_function(Client)), bg="#fff", relief="flat", bd=0, highlightthickness=0)
        self.app.place(relx=0.240, rely=0.4)
    # Chụp màn hình
        self.btnSCapture = PhotoImage(
            file='./img/button/screenCapture.png')                      # Đặt hình ảnh
        self.capture = Button(self.login,  image=self.btnSCapture, command=(
            lambda: self.screenCapture(Client)), bg="#fff", relief="flat", bd=0, highlightthickness=0)
        self.capture.place(relx=0.240, rely=0.758)
    # Keystroke
        self.btnKStroke = PhotoImage(
            file='./img/button/keyStroke.png')                      # Đặt hình ảnh
        self.key = Button(self.login, image=self.btnKStroke, command=(
            lambda: self.keyStroke(Client)), bg="#fff", relief="flat", bd=0, highlightthickness=0)
        self.key.place(relx=0.765, rely=0.4)
    # Tắt máy
        # Đặt hình ảnh
        self.btnSDwon = PhotoImage(file='./img/button/shutDown.png')
        self.shut = Button(self.login, image=self.btnSDwon, command=(
            lambda: self.shutDown(Client)), bg="#fff", relief="flat", bd=0, highlightthickness=0)
        self.shut.place(relx=0.245, rely=0.58)
    # Thoát
        # Đặt hình ảnh
        self.btnExist = PhotoImage(file='./img/button/exit.png')
        self.escape = Button(self.login, image=self.btnExist, command=(
            lambda: self.Exit(Client)), bg="#fff", relief="flat", bd=0, highlightthickness=0)
        self.escape.place(relx=0.505, rely=0.58)

# Hàm chụp ảnh màn hình
    def screenCapture(self, Client):
        try:
            screenCapture_Client.screencapture(Client)  # Đọc hàm screenCapture
        except:
            # Thông báo lỗi nếu hàm lỗi
            messagebox.showinfo("Error !!!", "Lỗi kết nối")

# Hàm khởi động các chương trình (Watch, Kill, Start)
    def application_function(self, Client):
        try:
            appRunning_Client.application_function(
                self, Client)  # Đọc hàm application_function
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")

# Hàm khởi động các process (Watch, Kill, Start)
    def process_function(self, Client):
        try:
            processRunning_Client.processrunning(Client)  # Đọc hàm process_function
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")

# Hàm theo dõi bàn phím (Hoạt động như Keylogger)
    def keyStroke(self, Client):
        try:
            # Đọc hàm keystroke của file Keystroke_Client.py
            Keystroke_Client.keystroke(Client)
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")

# Hàm Shutdown
    def shutDown(self, Client):
        try:
            # Gửi thông điệp "shut down" đến server, server sẽ tự động tắt máy trong 30s
            Client.send(bytes("Shutdown", 'utf-8'))
            # send(): 	Phương thức này truyền TCP message.
            # Thông báo thành công
            messagebox.showinfo("Success", "Máy tính sẽ tắt sau 40s")
        except:
            # Nếu lỗi kết nối thì thông báo lỗi
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")

# Hàm thoát	chương trình
    def Exit(self, Client):
        try:
            # Gửi thông điệp để thoát khỏi chương trình
            Client.send(bytes("Exit", 'utf-8'))
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")
        Client.close()							# Đóng kết nối
        self.Home.destroy()						# Đóng cửa sổ

# Hàm xử lý kết nối giữa Client - Server
    def Connection_handling(self, HOST):
        PORT = 1234						# Đặt cổng kết nối
        Client = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)       # Tạo socket
    # Kiểm tra lỗi kết nối bằng cách dùng try và except
        try:
            Client.connect((HOST, PORT))				# Kết nối tới server
            # Client.send(bytes("Success", 'utf-8'))		# Gửi thông điệp thành công
            # Nếu đúng sẽ hiển thị thông báo thành công
            messagebox.showinfo("Successful !!!", "Kết nối server thành công")
            # Sau đó gọi đến hàm Controller để hiển thị các nút điều khiển
            rcv = Thread(target=self.Controller(Client))
            rcv.start()				# Khởi động luồng
        except:
            # Nếu lỗi thì in ra màn hình, sau đó đóng kết nối client
            messagebox.showinfo(" Error!!!", "Không thể kết nối đến server")
            Client.close()


if __name__ == "__main__":		# Nếu chương trình được chạy tự động thì sẽ chạy hàm main
    Main()						# Gọi hàm Main để hiển thị các nút điều khiển
