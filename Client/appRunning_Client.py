from tkinter import Tk, W, E
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import ttk
from tkinter import *
from tkinter import messagebox


class Application:
    def __init__(self, client):
        self.app = Tk()
        self.app.title("App Running")
        self.app.configure(bg="white")
        self.app.iconbitmap('./img/button/remoteIcon.ico')

        self.client = client
        self.app_activity = None

        self.create_widgets()

    def create_widgets(self):
        start_button = Button(self.app, text="Start", font="Helvetica 10 bold", padx=30, pady=20,         
                              command=self.start_app, bd=5, bg="#000940", fg="#fff", activebackground='#fff')  # Định dạng button start
        start_button.grid(row=0, column=0, padx=8) # Vi trí của button trong grid

        watch_button = Button(self.app, text="Watch", font="Helvetica 10 bold", padx=30, pady=20,  
                      command=lambda: self.watch_app(self.client), bd=5, bg="#000940", fg="#fff", activebackground='#fff') # Định dạng button watch
        watch_button.grid(row=0, column=1, padx=8) # Vị trí của button trong grid

        kill_button = Button(self.app, text="Kill", font="Helvetica 10 bold", padx=30, pady=20,
                             command=self.kill_app, bd=5, bg="#000940", fg="#fff", activebackground='#fff') # Định dạng button kill
        kill_button.grid(row=0, column=2, padx=8)   # Vị trí của button trong grid

        delete_button = Button(self.app, text="Delete", font="Helvetica 10 bold", padx=30, pady=20,
                               command=self.clear, bd=5, bg="#000940", fg="#fff", activebackground='#fff') # Định dạng button delete
        delete_button.grid(row=0, column=3, padx=8) # Vị trí của button trong grid

    def clear(self):     # Hàm clear để dọn dẹp các tiến trình hiện tại để thay các tiến trình khác
        if self.app_activity:
            self.app_activity.destroy()  # X

    def watch_app(self,client):
        global app_activity                    # Khai báo biến process_activity
        global PORT                             # Khai báo biến PORT
        PORT = 1235
        self.length = 0                         # Khai báo biến length
        self.ID = [''] * 1000                   # Khai báo biến ID
        self.Name = [''] * 1000                 # Khai báo biến Name
        self.Thread = [''] * 1000
        try:
            # Gửi thông điệp Watch_AppRunning
            client.sendall(bytes("Watch_AppRunning", "utf-8"))
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
            # Vòng lặp để nhận dữ liệu cho data
            for i in range(self.length):
                self.data = client.recv(1024).decode(
                    "utf-8")       # Nhận dữ liệu từ server
                # Chuyển dữ liệu từ string sang int
                self.ID[i] = self.data
                # Gửi dữ liệu từ client lên server
                client.sendall(bytes(self.data, "utf-8"))

            # Vòng lặp để nhận dữ liệu cho name
            for i in range(self.length):
                self.data = client.recv(1024).decode(
                    "utf-8")       # Nhận dữ liệu từ server
                # Chuyển dữ liệu từ string sang int
                self.Name[i] = self.data
                # Gửi dữ liệu từ client lên server
                client.sendall(bytes(self.data, "utf-8"))

            # Vòng lặp để nhận dữ liệu cho thread
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

        self.app_activity = Frame(
            self.app, bg="white", padx=20, pady=20, borderwidth=5)
        self.app_activity.grid(row=1, columnspan=5, padx=20)

        # Khai báo scrollbar
        self.scrollbar = Scrollbar(self.app_activity)
        self.scrollbar.pack(side=RIGHT, fill=Y)                 # Đặt scrollbar
        # Khai báo treeview
        self.mybar = ttk.Treeview(
            self.app_activity, yscrollcommand=self.scrollbar.set)
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
        self.mybar.heading("#0", text="App Name", anchor=W)
        # Đặt tiêu đề cột 1
        self.mybar.heading("1", text="ID", anchor=CENTER)
        # Đặt tiêu đề cột 2
        self.mybar.heading("2", text="Thread", anchor=CENTER)
        for i in range(self.length):
            self.mybar.insert(parent='', index='end', iid=0+i, text=self.Name[i], values=(
                self.ID[i], self.Thread[i])) 

    def kill_app(self):
        self.clear()  
        self.screen_KA = Tk()
        self.screen_KA.geometry("320x100")
        self.screen_KA.title("Kill")
        self.Name_input = Entry(self.screen_KA, width=35)
        self.Name_input.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.Name_input.insert(END, "Nhập tên")
        Kill_Button = Button(self.screen_KA, text="Kill", bg="#000940", fg="#fff", font="Helvetica 10 bold", padx=20, command=self.kill_func,
                             bd=5, activebackground='#877776')
        Kill_Button.grid(row=0, column=4, padx=5, pady=5)
        
    def kill_func(self):
        self.AppName = self.Name_input.get()                
        self.client.sendall(bytes("Kill_Task", "utf-8"))    
        self.client.sendall(bytes(self.AppName, "utf-8"))  
        self.checkdata = self.client.recv(1024).decode("utf-8") 
        if self.checkdata == "Deleted":
            messagebox.showinfo("", "Chương trình đã tắt")
        else:
            messagebox.showinfo("Error !!!", "Không tìm thấy chương trình") 

    def start_app(self):
        self.screen_Start = Toplevel(self.app)
        self.screen_Start.geometry("320x100")
        self.screen_Start.title("Start")
        self.Name_input = Entry(self.screen_Start, width=35)
        self.Name_input.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.Name_input.insert(END, "Nhập Tên")
        Start_Button = Button(self.screen_Start, text="Start", bg="#000940", fg="#fff", font="Helvetica 10 bold", padx=20,
                            command=self.press_start, bd=5, activebackground='#836264')
        Start_Button.grid(row=0, column=4, padx=5, pady=5)

    def press_start(self):
        self.Name = self.Name_input.get()
        self.client.sendall(bytes("OpenTask", "utf-8"))
        
        self.client.sendall(bytes(self.Name, "utf-8"))
        self.checkdata = self.client.recv(1024).decode("utf-8")
        
        if self.checkdata == "opened":
            messagebox.showinfo("", "Chương trình đã bật")
        else:
            messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")


def apprunning(client):
    apprunning_client = Application(client)
    apprunning_client.app.mainloop()
