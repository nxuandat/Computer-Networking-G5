from threading import Thread
import socket
import os
import pyautogui
from tkinter import *
import Keystroke_SV

PORT = 3000
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVER.bind((SERVER_IP, PORT))
print("Server đang chạy: ", (SERVER_IP))


def read_Request(Client):
    request = ""
    try:
        request = Client.recv(1024).decode(
            'utf-8')
    except:
        print("Error !!!, Không nhận được yêu cầu từ client")
    finally:
        return request


def take_Request(Client):
    while True:
        Request = read_Request(Client)
        print("====> Yêu cầu từ server: ", Request)
        if not Request:
            Client.close()
            break

        if "screenCapture" == Request:
            image = pyautogui.screenshot()
            new_image = image.resize((1084, 530))
            new_image.save("picture.png")
            try:
                myfile = open("picture.png", 'rb')
                bytess = myfile.read()

                Client.sendall(bytess)
                myfile.close()
            except:
                print("Không chụp được màn hình")

        elif "Watch_ProcessRunning" == Request:
            import subprocess
            cmd = 'powershell "Get-Process |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
            ProccessProc = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE)

            count = 0
            length = 0
            Name = ['' for i in range(10000)]
            ID = ['' for i in range(10000)]
            Thread = ['' for i in range(10000)]
            for line in ProccessProc.stdout:
                if line.rstrip():
                    if count < 2:
                        count += 1
                        continue
                    msg = str(line.decode().rstrip().lstrip())
                    msg = " ".join(msg.split())
                    lists = msg.split(" ", 3)
                    ID[length] = lists[0]
                    Name[length] = lists[1]
                    Thread[length] = lists[2]
                    length += 1

            Client.sendall(bytes(str(length), "utf-8"))

            for i in range(length):
                Client.sendall(bytes(ID[i], "utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Name[i], "utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Thread[i], "utf-8"))
                checkdata = Client.recv(1024)

        elif "Watch_AppRunning" == Request:
            import subprocess
            cmd = 'powershell "Get-Process |where {$_.mainWindowTItle} |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
            openCMD = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE)
            count = 0
            length = 0
            Name = ['' for i in range(100)]
            ID = ['' for i in range(100)]
            Thread = ['' for i in range(100)]
            for line in openCMD.stdout:
                if line.rstrip():
                    if count < 2:
                        count += 1
                        continue
                    msg = str(line.decode().rstrip().lstrip())
                    msg = " ".join(msg.split())
                    lists = msg.split(" ", 3)
                    ID[length] = lists[0]
                    Name[length] = lists[1]
                    Thread[length] = lists[2]
                    length += 1

            Client.sendall(bytes(str(length), "utf-8"))

            for i in range(length):
                Client.sendall(bytes(ID[i], "utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Name[i], "utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Thread[i], "utf-8"))
                checkdata = Client.recv(1024)

        elif "OpenTask" == Request:
            import subprocess
            mode = 0o666
            flags = os.O_RDWR | os.O_CREAT
            m = Client.recv(1024)
            msg = str(m)
            msg = msg[2:]
            msg = msg[:len(msg)-1]

            try:
                cmd = 'powershell start ' + msg
                subprocess.run(cmd, check=True)
                Client.send(bytes("opened", "utf-8"))
            except subprocess.CalledProcessError:
                Client.send(bytes("Not found", "utf-8"))

        elif "Kill_Task" == Request:
            m = Client.recv(1024)
            msg = str(m)
            msg = msg[2:]
            msg = msg[:len(msg)-1]
            print(str(msg))
            from subprocess import call
            taskkillexe = "c:/windows/system32/taskkill.exe"
            taskkillparam = (taskkillexe, '/F',  '/IM', msg + '.exe')
            taskkillexitcode = call(taskkillparam)

            if taskkillexitcode == 0:
                Client.send(bytes("Deleted", "utf-8"))
            else:
                Client.send(bytes("Not found", "utf-8"))

        elif "HookKey" == Request:
            Client.sendall(bytes("Đã nhận", "utf-8"))
            Keystroke_SV.Keystroke(Client)

        elif "Shutdown" == Request:
            os.system("shutdown /s /t 40")

        elif "Exit" == Request:
            Client.sendall(bytes("Đã thoát", "utf-8"))
            break


def waiting():
    print("Chờ các kết nối từ client...")
    while True:
        client, Address = SERVER.accept()
        print("Client", Address, "---> Đã kết nối !!!")
        Thread(target=take_Request, args=(client,)
               ).start()


def listenAndclose():
    try:
        SERVER.listen()
        ACCEPT_THREAD = Thread(target=waiting())
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    except:
        print("Error !!!, Server đã dừng")
    finally:
        SERVER.close()


def interface():
    top = Tk()
    top.title("Server Connection")
    top.geometry("500x300")
    top.configure(bg="#000940")
    top.iconbitmap('./img/button/remoteIcon.ico')
    btn1 = PhotoImage(file='./img/button/anh2a.png')
    btn2 = PhotoImage(file='./img/button/anh1a.png')

    def on_enter(event):
        top.button.config(image=btn2)

    def on_leave(event):
        top.button.config(image=btn1)

    top.button = Button(top, image=btn1, bg="#fff", command=listenAndclose,
                        relief="flat", bd=0, highlightthickness=0, activebackground="#f7f7f7")
    top.button.pack(pady=5, padx=5, expand=True)

    top.button.bind("<Enter>", on_enter)
    top.button.bind("<Leave>", on_leave)
    top.mainloop()


if __name__ == "__main__":
    interface()
