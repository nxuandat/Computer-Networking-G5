from tkinter import Tk, Entry, Button, messagebox, END




class ProcessWindow:       
    def __init__(self, client):         # Tạo cửa sổ GUI từ phương pháp _init_ và thiết lập cài đăt ban đầu 
        self.process = Tk()
        self.process.title("Process Running")
        self.process.configure(bg="#FFFAF0")
        self.process.iconbitmap('./img/button/remoteIcon.ico')

        self.client = client
        self.process_activity = None

        self.create_widgets()  

    def create_widgets(self): # Hàm create_widgets tạo các button để thực hiện các chức năng bên dưới
        start_button = Button(self.process, text="Start", font="Helvetica 10 bold", padx=30, pady=20,                   # Định dạng cho các button
                              command=self.start_process, bd=5, bg="#000940", fg="#fff", activebackground='#fff')
        start_button.grid(row=0, column=0, padx=8)

        watch_button = Button(self.process, text="Watch", font="Helvetica 10 bold", padx=30, pady=20,
                              command=self.watch_processes, bd=5, bg="#000940", fg="#fff", activebackground='#fff')
        watch_button.grid(row=0, column=1, padx=8)

        kill_button = Button(self.process, text="Kill", font="Helvetica 10 bold", padx=30, pady=20,
                             command=self.kill_process, bd=5, bg="#000940", fg="#fff", activebackground='#fff')
        kill_button.grid(row=0, column=2, padx=8)

        delete_button = Button(self.process, text="Delete", font="Helvetica 10 bold", padx=30, pady=20,
                               command=self.clear, bd=5, bg="#000940", fg="#fff", activebackground='#fff')
        delete_button.grid(row=0, column=3, padx=8)

    def clear(self):     # Hàm clear để dọn dẹp các tiến trình hiện tại để thay các tiến trình khác
        if self.process_activity:
            self.process_activity.destroy()

    def watch_processes(self): # Hàm watch_processes dùng để xem các chương trình
        self.clear()

        try:
            self.client.sendall(bytes("Watch_ProcessRunning", "utf-8"))
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối")
            self.process.destroy()

    def kill_process(self):     # Hàm kill_processes dùng để dừng các chương trình
        self.clear()                    # Tạo cửa sổ screen_KillTask khi button Kill được click
                                        # Yêu cầu nhập tên chương trình, 1 nút button dùng để xác nhận chương trình cần dừng 
        self.screen_KillTask = Tk()         
        self.screen_KillTask.geometry("320x50")
        self.screen_KillTask.title("Kill")

        self.Name_input = Entry(self.screen_KillTask, width=35)
        self.Name_input.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.Name_input.insert(END, "Nhập tên")

        Kill_Button = Button(self.screen_KillTask, bg="#000940", fg="#fff", text="Kill", font="Helvetica 10 bold",
                             padx=20, command=self.kill_func, bd=5, activebackground='#7c6e6c')
        Kill_Button.grid(row=0, column=4, padx=5, pady=5)

    def kill_func(self):        # Hàm kill_func thực hiện song song hàm kill_process, thực hiện để xác nhận Input cho vào
        self.AppName = self.Name_input.get()                # Nếu chương trình có tồn tại thì sẽ thực hiện kill_process vào thông báo thì kết thúc
        self.client.sendall(bytes("Kill_Task", "utf-8"))    # Ngược lại sẽ thông báo lỗi và không thực hiện hàm kill_process
        try:
            self.client.sendall(bytes(self.AppName, "utf-8"))
            self.checkdata = self.client.recv(1024).decode("utf-8")
            messagebox.showinfo("", "Đã đóng chương trình")
        except:
            messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")

    def start_process(self):    # Hàm start_process tương tự như kill_process nhưng là chạy chương trình thay vì dừng
        self.screen_Start = Tk()
        self.screen_Start.geometry("320x50")
        self.screen_Start.title("Start")

        self.Name_input = Entry(self.screen_Start, width=35)
        self.Name_input.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.Name_input.insert(END, "Nhập Tên")

        Start_Button = Button(self.screen_Start, text="Start", bg="#000940", fg="#fff", font="Helvetica 10 bold",
                              padx=20, command=self.press_start, bd=5)
        Start_Button.grid(row=0, column=4, padx=5, pady=5)

    def press_start(self):  # Hàm press_start tương tự kill_func , dùng để kiểm tra input nhập vào
        self.Name = self.Name_input.get()
        self.client.sendall(bytes("OpenTask", "utf-8"))
        try:
            self.client.sendall(bytes(self.Name, "utf-8"))
            self.checkdata = self.client.recv(1024).decode("utf-8")
            messagebox.showinfo("", "Chương trình đã bật")
        except:
            messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")


