from tkinter import Tk, Entry, Button, messagebox, END




class ProcessWindow:       
    def __init__(self, client):         # Tạo cửa sổ GUI từ phương pháp _init_ và thiết lập cài đăt ban đầu 
        self.process = Tk()
        self.process.title("Process Running") # Tựa đề
        self.process.configure(bg="#FFFAF0") # Background
        self.process.iconbitmap('./img/button/remoteIcon.ico') # Icon 

        self.client = client
        self.process_activity = None

        self.create_widgets()  # Thực hiện hàm

    def create_widgets(self): # Hàm create_widgets tạo các button để thực hiện các chức năng bên dưới
        start_button = Button(self.process, text="Start", font="Helvetica 10 bold", padx=30, pady=20,         
                              command=self.start_process, bd=5, bg="#000940", fg="#fff", activebackground='#fff')  # Định dạng button start
        start_button.grid(row=0, column=0, padx=8) # Vi trí của button trong grid

        watch_button = Button(self.process, text="Watch", font="Helvetica 10 bold", padx=30, pady=20,  
                              command=self.watch_processes, bd=5, bg="#000940", fg="#fff", activebackground='#fff') # Định dạng button watch
        watch_button.grid(row=0, column=1, padx=8) # Vị trí của button trong grid

        kill_button = Button(self.process, text="Kill", font="Helvetica 10 bold", padx=30, pady=20,
                             command=self.kill_process, bd=5, bg="#000940", fg="#fff", activebackground='#fff') # Định dạng button kill
        kill_button.grid(row=0, column=2, padx=8)   # Vị trí của button trong grid

        delete_button = Button(self.process, text="Delete", font="Helvetica 10 bold", padx=30, pady=20,
                               command=self.clear, bd=5, bg="#000940", fg="#fff", activebackground='#fff') # Định dạng button delete
        delete_button.grid(row=0, column=3, padx=8) # Vị trí của button trong grid

    def clear(self):     # Hàm clear để dọn dẹp các tiến trình hiện tại để thay các tiến trình khác
        if self.process_activity:
            self.process_activity.destroy()  # Xóa các tiến trình hiện tại

    def watch_processes(self): # Hàm watch_processes dùng để xem các chương trình
        self.clear()

        try:
            self.client.sendall(bytes("Watch_ProcessRunning", "utf-8"))  # Gửi lệnh Watch_ProcessRunning cho server
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối") # Thông báo lỗi
            self.process.destroy()

    def kill_process(self):     # Hàm kill_processes dùng để dừng các chương trình
        self.clear()                    # Tạo cửa sổ screen_KillTask khi button Kill được click
                                        # Yêu cầu nhập tên chương trình, 1 nút button dùng để xác nhận chương trình cần dừng 
        self.screen_KillTask = Tk()         
        self.screen_KillTask.geometry("320x50") # Kích thước
        self.screen_KillTask.title("Kill")  # Tên

        self.Name_input = Entry(self.screen_KillTask, width=35)   # Định dạng chỗ input
        self.Name_input.grid(row=0, column=0, columnspan=3, padx=5, pady=5) # Grid của input
        self.Name_input.insert(END, "Nhập tên") # Thêm "Nhập tên"

        Kill_Button = Button(self.screen_KillTask, bg="#000940", fg="#fff", text="Kill", font="Helvetica 10 bold",
                             padx=20, command=self.kill_func, bd=5, activebackground='#7c6e6c')  # Chức năng và định dạng cho button
        Kill_Button.grid(row=0, column=4, padx=5, pady=5) # grid cho button

    def kill_func(self):        # Hàm kill_func thực hiện song song hàm kill_process, thực hiện để xác nhận Input cho vào
        self.AppName = self.Name_input.get()                # Nếu chương trình có tồn tại thì sẽ thực hiện kill_process vào thông báo thì kết thúc
        self.client.sendall(bytes("Kill_Task", "utf-8"))    # Ngược lại sẽ thông báo lỗi và không thực hiện hàm kill_process
        try:
            self.client.sendall(bytes(self.AppName, "utf-8"))  # Gửi input cho server
            self.checkdata = self.client.recv(1024).decode("utf-8") # Kiểm tra input 
            messagebox.showinfo("", "Đã đóng chương trình")  # Thông báo 
        except:
            messagebox.showinfo("Error !!!", "Không tìm thấy chương trình") # Báo lỗi

    def start_process(self):    # Hàm start_process tương tự như kill_process nhưng là chạy chương trình thay vì dừng
        self.screen_Start = Tk()
        self.screen_Start.geometry("320x50") # Kích thước 
        self.screen_Start.title("Start")    # Tên

        self.Name_input = Entry(self.screen_Start, width=35) # Kích thước khung input
        self.Name_input.grid(row=0, column=0, columnspan=3, padx=5, pady=5) # Grid của input
        self.Name_input.insert(END, "Nhập Tên") # Thêm "Nhập tên"

        Start_Button = Button(self.screen_Start, text="Start", bg="#000940", fg="#fff", font="Helvetica 10 bold",
                              padx=20, command=self.press_start, bd=5) # Chức năng và định dạng cho button
        Start_Button.grid(row=0, column=4, padx=5, pady=5) # Grid cho button 

    def press_start(self):  # Hàm press_start tương tự kill_func , dùng để kiểm tra input nhập vào
        self.Name = self.Name_input.get()
        self.client.sendall(bytes("OpenTask", "utf-8"))
        try:
            self.client.sendall(bytes(self.Name, "utf-8"))
            self.checkdata = self.client.recv(1024).decode("utf-8")
            messagebox.showinfo("", "Chương trình đã bật")
        except:
            messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")


