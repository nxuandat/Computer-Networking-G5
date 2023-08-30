from tkinter import Tk, W
from tkinter.ttk import Frame, Button, Entry
from tkinter import ttk
from tkinter import *
from tkinter import messagebox


class ProcessWindow:
    def __init__(self, client):
        self.process = Tk()
        self.process.title("Process Running")
        self.process.configure(bg="#FFFAF0")
        self.process.iconbitmap('./img/button/remoteIcon.ico')

        self.client = client
        self.process_activity = None

        self.create_widgets()

    def create_widgets(self):
        start_button = Button(self.process, text="Start", font="Helvetica 10 bold", padx=30, pady=20,
                              command=self.start_process, bd=5, bg="#000940", fg="#fff", activebackground='#fff')
        start_button.grid(row=0, column=0, padx=8)

        watch_button = Button(self.process, text="Watch", font="Helvetica 10 bold", padx=30, pady=20,
                              command=lambda: self.watch_processes(self.client), bd=5, bg="#000940", fg="#fff", activebackground='#fff')
        watch_button.grid(row=0, column=1, padx=8)

        kill_button = Button(self.process, text="Kill", font="Helvetica 10 bold", padx=30, pady=20,
                             command=self.kill_process, bd=5, bg="#000940", fg="#fff", activebackground='#fff')
        kill_button.grid(row=0, column=2, padx=8)

        delete_button = Button(self.process, text="Delete", font="Helvetica 10 bold", padx=30, pady=20,
                               command=self.clear, bd=5, bg="#000940", fg="#fff", activebackground='#fff')
        delete_button.grid(row=0, column=3, padx=8)

    def clear(self):
        if self.process_activity:
            self.process_activity.destroy()

    def watch_processes(self, client):
        global process_activity
        global PORT
        PORT = 3000
        self.length = 0
        self.ID = [''] * 1000
        self.Name = [''] * 1000
        self.Thread = [''] * 1000
        try:
            client.sendall(bytes("Watch_ProcessRunning", "utf-8"))
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")
            self.process.destroy()

        try:
            self.length = client.recv(1024).decode(
                "utf-8")
            self.length = int(self.length)
            for i in range(self.length):
                self.data = client.recv(1024).decode(
                    "utf-8")
                self.ID[i] = self.data
                client.sendall(bytes(self.data, "utf-8"))

            for i in range(self.length):
                self.data = client.recv(1024).decode(
                    "utf-8")
                self.Name[i] = self.data
                client.sendall(bytes(self.data, "utf-8"))

            for i in range(self.length):
                self.data = client.recv(1024).decode(
                    "utf-8")
                self.Thread[i] = self.data
                client.sendall(bytes(self.data, "utf-8"))
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")

        self.process_activity = Frame(
            self.process, bg="white", padx=20, pady=20, borderwidth=5)
        self.process_activity.grid(row=1, columnspan=5, padx=20)

        self.scrollbar = Scrollbar(self.process_activity)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.mybar = ttk.Treeview(
            self.process_activity, yscrollcommand=self.scrollbar.set)
        self.mybar.pack()
        self.scrollbar.config(command=self.mybar.yview)

        self.mybar['columns'] = ("1", "2")
        self.mybar.column("#0", anchor=CENTER, width=200,
                          minwidth=25)
        self.mybar.column("1", anchor=CENTER, width=100)
        self.mybar.column("2", anchor=CENTER, width=100)

        self.mybar.heading("#0", text="Process Name", anchor=W)
        self.mybar.heading("1", text="ID", anchor=CENTER)
        self.mybar.heading("2", text="Thread", anchor=CENTER)
        for i in range(self.length):
            self.mybar.insert(parent='', index='end', iid=0+i, text=self.Name[i], values=(
                self.ID[i], self.Thread[i]))

    def kill_process(self):
        self.clear()
        self.screen_KillTask = Tk()
        self.screen_KillTask.geometry("320x50")
        self.screen_KillTask.title("Kill")

        self.Name_input = Entry(self.screen_KillTask, width=35)
        self.Name_input.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.Name_input.insert(END, "Nhập tên")

        Kill_Button = Button(self.screen_KillTask, bg="#000940", fg="#fff", text="Kill", font="Helvetica 10 bold",
                             padx=20, command=self.kill_func, bd=5, activebackground='#7c6e6c')
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

    def start_process(self):
        self.screen_Start = Tk()
        self.screen_Start.geometry("320x50")
        self.screen_Start.title("Start")

        self.Name_input = Entry(self.screen_Start, width=35)
        self.Name_input.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.Name_input.insert(END, "Nhập Tên")

        Start_Button = Button(self.screen_Start, text="Start", bg="#000940", fg="#fff", font="Helvetica 10 bold",
                              padx=20, command=self.press_start, bd=5)
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


def processrunning(client):
    processrunning_client = ProcessWindow(client)
    processrunning_client.process.mainloop()
