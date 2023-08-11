from tkinter import Tk, W, E
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import ttk
from tkinter import *
from tkinter import messagebox


def process_function(self, client):
    self.process = Tk()
    self.process.title("Process Running")       # Tựa đề của cửa sổ
    self.process.configure(bg="#FFFAF0")        # Màu nền
    self.process.iconbitmap('./img/button/remoteIcon.ico')
# Hàm clear màn hình

    def Clear():
        self.process_activity.destroy()            # Xóa process_activity
# Hàm hiển thị các process đang chạy

    def Watch_Processes():
        global process_activity                    # Khai báo biến process_activity
        global PORT                             # Khai báo biến PORT
        PORT = 1234                             # Khai báo PORT
        self.length = 0                         # Khai báo biến length
        self.ID = [''] * 1000                   # Khai báo biến ID
        self.Name = [''] * 1000                 # Khai báo biến Name
        self.Thread = [''] * 1000               # Khai báo biến Thread
        try:
            # Gửi thông điệp Watch_ProcessRunning
            client.sendall(bytes("Watch_ProcessRunning", "utf-8"))
        except:
            # Thông báo lỗi
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")
            self.process.destroy()                                  # Xóa cửa sổ

        # Receive data
        try:
            self.length = client.recv(1024).decode(
                "utf-8")         # Nhận dữ liệu từ server
            # Chuyển dữ liệu từ string sang int
            self.length = int(self.length)
            # Vòng lặp để nhận dữ liệu
            for i in range(self.length):
                self.data = client.recv(1024).decode(
                    "utf-8")       # Nhận dữ liệu từ server
                # Chuyển dữ liệu từ string sang int
                self.ID[i] = self.data
                # Gửi dữ liệu từ client lên server
                client.sendall(bytes(self.data, "utf-8"))

            # Vòng lặp để nhận dữ liệu
            for i in range(self.length):
                self.data = client.recv(1024).decode(
                    "utf-8")       # Nhận dữ liệu từ server
                # Chuyển dữ liệu từ string sang int
                self.Name[i] = self.data
                # Gửi dữ liệu từ client lên server
                client.sendall(bytes(self.data, "utf-8"))

            # Vòng lặp để nhận dữ liệu
            for i in range(self.length):
                self.data = client.recv(1024).decode(
                    "utf-8")       # Nhận dữ liệu từ server
                # Chuyển dữ liệu từ string sang int
                self.Thread[i] = self.data
                # Gửi dữ liệu từ client lên server
                client.sendall(bytes(self.data, "utf-8"))
        except:
            # Thông báo lỗi
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")

        self.process_activity = Frame(
            self.process, bg="white", padx=20, pady=20, borderwidth=5)
        self.process_activity.grid(row=1, columnspan=5, padx=20)

        # Khai báo scrollbar
        self.scrollbar = Scrollbar(self.process_activity)
        self.scrollbar.pack(side=RIGHT, fill=Y)                 # Đặt scrollbar
        # Khai báo treeview
        self.mybar = ttk.Treeview(
            self.process_activity, yscrollcommand=self.scrollbar.set)
        self.mybar.pack()                                       # Đặt treeview
        self.scrollbar.config(command=self.mybar.yview)         # Đặt scrollbar

        self.mybar['columns'] = ("1", "2")                      # Khai báo cột
        self.mybar.column("#0", anchor=CENTER, width=200,
                          minwidth=25)                          # Đặt cột #0
        # Đặt cột 1
        self.mybar.column("1", anchor=CENTER, width=100)
        # Đặt cột 2
        self.mybar.column("2", anchor=CENTER, width=100)

        # Đặt tiêu đề cột #0
        self.mybar.heading("#0", text="Process Name", anchor=W)
        # Đặt tiêu đề cột 1
        self.mybar.heading("1", text="ID", anchor=CENTER)
        # Đặt tiêu đề cột 2
        self.mybar.heading("2", text="Thread", anchor=CENTER)
        for i in range(self.length):
            self.mybar.insert(parent='', index='end', iid=0+i, text=self.Name[i], values=(
                self.ID[i], self.Thread[i]))                      # Đặt dữ liệu cột 1
# Hàm dừng 1 process

    def Kill_Process():
        self.screen_KillTask = Tk()                     # Khai báo cửa sổ
        self.screen_KillTask.geometry("320x50")         # Đặt kích thước cửa sổ
        self.screen_KillTask.title("Kill")              # Đặt tiêu đề cửa sổ

        self.Name_input = Entry(self.screen_KillTask,
                                width=35)          # Khai báo Entry
        self.Name_input.grid(row=0, column=0, columnspan=3,
                             padx=5, pady=5)          # Đặt Entry
        # Đặt giá trị mặc định
        self.Name_input.insert(END, "Nhập tên")

        Kill_Button = Button(self.screen_KillTask, bg="#000940", fg="#fff", text="Kill", font="Helvetica 10 bold", padx=20,
                             command=Kill_Func, bd=5, activebackground='#7c6e6c').grid(row=0, column=4, padx=5, pady=5)      # Khai báo nút Kill

    def Kill_Func():
        # Lấy giá trị của Entry
        self.AppName = self.Name_input.get()
        # Gửi dữ liệu từ client lên server
        client.sendall(bytes("Kill_Task", "utf-8"))
        try:
            # Gửi dữ liệu từ client lên server
            client.sendall(bytes(self.AppName, "utf-8"))
            self.checkdata = client.recv(1024).decode(
                "utf-8")      # Nhận dữ liệu từ server
            # recv(): 	Phương thức này nhận TCP message.
            # Thông báo đã đóng chương trình
            messagebox.showinfo("", "Đã đóng chương trình")
        except:
            messagebox.showinfo(
                "Error !!!", "Không tìm thấy chương trình")     # Thông báo lỗi

# Hàm khởi động 1 process
    def Start_Process():
        self.screen_Start = Tk()
        self.screen_Start.geometry("320x50")
        self.screen_Start.title("Start")

        self.Name_input = Entry(self.screen_Start, width=35)
        self.Name_input.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        # Đặt giá trị mặc định
        self.Name_input.insert(END, "Nhập Tên")

        Start_Button = Button(self.screen_Start, text="Start", bg="#000940", fg="#fff", font="Helvetica 10 bold",
                              padx=20, command=PressStart, bd=5).grid(row=0, column=4, padx=5, pady=5)

    def PressStart():
        self.Name = self.Name_input.get()                    # Lấy giá trị của Entry
        # Gửi dữ liệu từ client lên server
        client.sendall(bytes("OpenTask", "utf-8"))
        try:
            # Gửi dữ liệu từ client lên server
            client.sendall(bytes(self.Name, "utf-8"))
            self.checkdata = client.recv(1024).decode(
                "utf-8")  # Nhận dữ liệu từ server
            # Thông báo đã bật chương trình
            messagebox.showinfo("", "Chương trình đã bật")
        except:
            messagebox.showinfo(
                "Error !!!", "Không tìm thấy chương trình")   # Thông báo lỗi

    Start = Button(self.process, text="Start", font="Helvetica 10 bold", padx=30, pady=20, command=Start_Process,
                   bd=5, bg="#000940", fg="#fff", activebackground='#fff').grid(row=0, column=0, padx=8)
    Watch = Button(self.process, text="Watch", font="Helvetica 10 bold", padx=30, pady=20, command=Watch_Processes,
                   bd=5, bg="#000940", fg="#fff", activebackground='#fff').grid(row=0, column=1, padx=8)
    Kill = Button(self.process, text="Kill", font="Helvetica 10 bold", padx=30, pady=20, command=Kill_Process,
                  bd=5, bg="#000940", fg="#fff", activebackground='#fff').grid(row=0, column=2, padx=8)
    Delete = Button(self.process, text="Delete", font="Helvetica 10 bold", padx=30, pady=20, command=Clear,
                    bd=5, bg="#000940", fg="#fff", activebackground='#fff').grid(row=0, column=3, padx=8)
