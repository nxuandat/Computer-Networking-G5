from threading import Thread
import socket       # thư viện socket
import os           # các chức năng được sử dụng để tương tác với hệ điều hành và cũng có được thông tin liên quan về nó
import pyautogui    # hỗ trợ đa nền tảng để quản lý hoạt động của chuột, bàn phím, chụp ảnh màn hình, tự động kiểm tra GUI,... thông qua mã để cho phép tự động hóa các tác vụ
from tkinter import *
import Keystroke_SV

PORT = 1234     # Đặt cổng kết nối
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Tạo socket
# Tạo địa chỉ IP server và thiết lập công kết nối
SERVER.bind((SERVER_IP, PORT))
# In ra địa chỉ server
print("Server đang chạy: ", (SERVER_IP))


def read_Request(Client):   # Hàm đọc yêu cầu từ client
    request = ""
    try:
        request = Client.recv(1024).decode(
            'utf-8')     # Nhận yêu cầu từ phía client
        # recv(): 	Phương thức này nhận TCP message.
    except:
        print("Error !!!, Không nhận được yêu cầu từ client")
    finally:
        return request


def take_Request(Client):   # Hàm nhận yêu cầu từ client
    while True:
        Request = read_Request(Client)
        print("====> Yêu cầu từ server: ", Request)
        if not Request:
            Client.close()
            break

        # Chụp màn hình rồi gửi lại cho client
        if "screenCapture" == Request:
            image = pyautogui.screenshot()                  # Chụp màn hình
            new_image = image.resize((1084, 530))
            new_image.save("picture.png")                       # Lưu ảnh
            try:
                myfile = open("picture.png", 'rb')          # Mở file dạng byte
                bytess = myfile.read()                      # Đọc file
                # Gửi file cho client
                Client.sendall(bytess)
                myfile.close()
            except:
                print("Không chụp được màn hình")

        elif "Watch_ProcessRunning" == Request:
            import subprocess
            # Lệnh powershell để lấy thông tin của các process đang chạy
            # powershell -> chạy lệnh trên powershell
            # Get-Process -> lấy thông tin của các process
            # Select-Object id, name -> lựa chọn các thông tin cần lấy
            # @{Name=\'ThreadCount\'} -> tên của thuộc tính
            # Expression ={$_.Threads.Count}} -> lấy giá trị của thuộc tính
            # format-table -> định dạng của dữ liệu (dạng bảng)
            cmd = 'powershell "Get-Process |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
            ProccessProc = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE)            # Tạo process
            # Đếm số lượng process
            count = 0
            # Đếm chiều dài của process
            length = 0
            # Tạo mảng chứa tên process
            Name = ['' for i in range(10000)]
            # Tạo mảng chứa ID process
            ID = ['' for i in range(10000)]
            # Tạo mảng chứa số lượng thread
            Thread = ['' for i in range(10000)]
            for line in ProccessProc.stdout:                                        # Đọc dữ liệu từ process
                if line.rstrip():                                                   # Xóa kí tự trắng
                    if count < 2:                                                   # Đếm số lượng process
                        count += 1                                                  # Đếm số lượng process
                        continue                                                    # Bỏ qua dòng đầu tiên
                    # Chuyển dữ liệu từ bytes sang string
                    msg = str(line.decode().rstrip().lstrip())
                    # Xóa kí tự trắng
                    msg = " ".join(msg.split())
                    # Tách dữ liệu theo khoảng trắng
                    lists = msg.split(" ", 3)
                    # Lấy ID process
                    ID[length] = lists[0]
                    # Lấy tên process
                    Name[length] = lists[1]
                    # Lấy số lượng thread
                    Thread[length] = lists[2]
                    # Đếm chiều dài của process
                    length += 1

            # Gửi số lượng process
            Client.sendall(bytes(str(length), "utf-8"))

            for i in range(length):
                # Gửi ID process về client
                Client.sendall(bytes(ID[i], "utf-8"))
                # recv(): 	Phương thức này nhận TCP message.
                checkdata = Client.recv(1024)
            for i in range(length):
                # Gửi tên process về client
                Client.sendall(bytes(Name[i], "utf-8"))
                # recv(): 	Phương thức này nhận TCP message.
                checkdata = Client.recv(1024)
            for i in range(length):
                # Gửi số lượng thread về client
                Client.sendall(bytes(Thread[i], "utf-8"))
                # Nhận dữ liệu từ client
                checkdata = Client.recv(1024)

        elif "Watch_AppRunning" == Request:
            import subprocess
            # Lệnh powershell để lấy thông tin của các app đang chạy
            # Sự khác nhau giữa Watch_ProcessRunning và Watch_AppRunning là:
            # where {$_.mainWindowTItle} -> lấy tên của app
            # -> Ở Process thì không cần lệnh này
            cmd = 'powershell "Get-Process |where {$_.mainWindowTItle} |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
            openCMD = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE)                 # Gọi cmd
            count = 0
            length = 0
            # Tạo mảng chứa tên process
            Name = ['' for i in range(100)]
            # Tạo mảng chứa ID process
            ID = ['' for i in range(100)]
            # Tạo mảng chứa số lượng thread
            Thread = ['' for i in range(100)]
            for line in openCMD.stdout:                             # Duyệt dữ liệu
                if line.rstrip():                                   # Kiểm tra dữ liệu
                    if count < 2:                         # Kiểm tra dữ liệu đầu tiên
                        count += 1                       # Đếm số lượng dòng
                        continue                             # Bỏ qua dòng đầu tiên
                    # Chuyển dữ liệu từ bytes sang string
                    msg = str(line.decode().rstrip().lstrip())
                    # Xóa khoảng trắng
                    msg = " ".join(msg.split())
                    # Chuyển dữ liệu thành mảng
                    lists = msg.split(" ", 3)
                    # Lấy ID process
                    ID[length] = lists[0]
                    # Lấy tên process
                    Name[length] = lists[1]
                    # Lấy số lượng thread
                    Thread[length] = lists[2]
                    length += 1                                                # Đếm số lượng process

            # Gửi số lượng process
            Client.sendall(bytes(str(length), "utf-8"))

            for i in range(length):
                # Gửi ID process
                Client.sendall(bytes(ID[i], "utf-8"))
                # Nhận dữ liệu từ client
                checkdata = Client.recv(1024)
            for i in range(length):
                # Gửi tên process
                Client.sendall(bytes(Name[i], "utf-8"))
                # Nhận dữ liệu từ client
                checkdata = Client.recv(1024)
            for i in range(length):
                # Gửi số lượng thread
                Client.sendall(bytes(Thread[i], "utf-8"))
                # Nhận dữ liệu từ client
                checkdata = Client.recv(1024)

        elif "OpenTask" == Request:  # Mở app
            import subprocess
            # Thiết lập mode (quyền truy cập tệp bát phân. 0o trong ES6 đại diện hệ bát phân)
            mode = 0o666
            # Thiết lập cờ (cờ đọc và ghi)
            flags = os.O_RDWR | os.O_CREAT
            # Nhận yêu cầu mở app/process
            m = Client.recv(1024)
            # Chuyển dữ liệu từ bytes sang string
            msg = str(m)
            # Xóa kí tự 'b' từ đầu dữ liệu
            msg = msg[2:]
            # Xóa kí tự '\n' đầu dữ liệu
            msg = msg[:len(msg)-1]
            
            try:
                cmd = 'powershell start ' + msg                 # Tạo process
                # Gọi process và thực thi
                subprocess.run(cmd, check=True)
                # Gửi thông báo đã mở
                Client.send(bytes("opened", "utf-8"))
                # send(): 	Phương thức này truyền TCP message.
            except subprocess.CalledProcessError:
                # Gửi thông báo không tìm thấy
                Client.send(bytes("Not found", "utf-8"))
                # send(): 	Phương thức này truyền TCP message.

        elif "Kill_Task" == Request:  # Xóa
            m = Client.recv(1024)                           # Nhận ID process
            # Chuyển dữ liệu từ bytes sang string
            msg = str(m)
            # Xóa kí tự 'b' từ đầu dữ liệu
            msg = msg[2:]
            msg = msg[:len(msg)-1]                          # Xóa kí tự '\n'
            print(str(msg))                                 # In ID process
            # Import thư viện call để gọi lệnh kill process
            from subprocess import call
            taskkillexe = "c:/windows/system32/taskkill.exe"            # Đường dẫn taskkill.exe
            # Truyền tham số vào taskkill.exe
            taskkillparam = (taskkillexe, '/F',  '/IM', msg + '.exe')
            taskkillexitcode = call(taskkillparam)          # Gọi taskkill.exe
            
            if taskkillexitcode == 0:
                # Gửi thông báo đã xóa
                Client.send(bytes("Deleted", "utf-8"))
            else:
                # Gửi thông báo lỗi khi không tìm thấy file
                Client.send(bytes("Not found", "utf-8"))

        elif "HookKey" == Request:                                                            # Hook key
            # Gửi thông báo đã nhận
            Client.sendall(bytes("Đã nhận", "utf-8"))
            # Gọi hàm Keystroke
            Keystroke_SV.Keystroke(Client)

        elif "Shutdown" == Request:
            os.system("shutdown /s /t 40")            # Tắt máy trong vòng 40s

        elif "Exit" == Request:
            # Gửi thông báo đã thoát
            Client.sendall(bytes("Đã thoát", "utf-8"))
            break


def waiting():    # Hàm chờ kết nối
    print("Chờ các kết nối từ client...")
    while True:
        client, Address = SERVER.accept()        # Chờ kết nối từ client
        # accept(): Phương thức này chấp nhận một cách thụ động kết nối TCP Client, đợi cho tới khi kết nối tới.
        print("Client", Address, "---> Đã kết nối !!!")
        Thread(target=take_Request, args=(client,)
               ).start()       # Tạo thread cho client


def listenAndclose():
    try:
        SERVER.listen()        # Đợi kết nối
        ACCEPT_THREAD = Thread(target=waiting())        # Tạo thread
        ACCEPT_THREAD.start()  # Khởi động thread
        ACCEPT_THREAD.join()  # Đợi cho thread kết thúc
    except:
        print("Error !!!, Server đã dừng")
    finally:
        SERVER.close()          # Đóng socket


def interface():   # Giao diện
    # Tạo cửa sổ
    top = Tk()
    # Đặt tiêu đề
    top.title("Server Connection")
    # Đặt kích thước
    top.geometry("500x300")
    top.configure(bg="#000940")
    top.iconbitmap('./img/button/remoteIcon.ico')
    # Đặt hình ảnh
    btn1 = PhotoImage(file='./img/button/anh2a.png')
    btn2 = PhotoImage(file='./img/button/anh1a.png')

    def on_enter(event):
        top.button.config(image=btn2)   # Hình hiển thị khi chưa hover

    def on_leave(event):
        top.button.config(image=btn1)   # Hình hiển thị khi hover

    top.button = Button(top, image=btn1, bg="#fff", command=listenAndclose,
                        relief="flat", bd=0, highlightthickness=0, activebackground="#f7f7f7")
    # Đặt kích thước và vị trí
    top.button.pack(pady=5, padx=5, expand=True)

    top.button.bind("<Enter>", on_enter)  # Đặt sự kiện khi chuột đến button
    # Đặt sự kiện khi chuột ra khỏi button
    top.button.bind("<Leave>", on_leave)
    top.mainloop()


if __name__ == "__main__":          # Chạy chương trình
    interface()
