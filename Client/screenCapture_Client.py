import os
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image


class ScreenCapture:
    def __init__(self, client):
        self.client = client
        self.Screenshot = Toplevel()
        self.Screenshot.title("ScreenShot")
        self.Screenshot.resizable(width=False, height=False)
        self.Screenshot.iconbitmap('./img/button/remoteIcon.ico')
        self.Screenshot.configure(bg="#C0C0C0", width=1090, height=610)

        self.canvas = Canvas(self.Screenshot, bg="white", width=1084, height=531)   # Tạo khung ảnh
        self.canvas.place(relx=0, rely=0)   

        self.btnChup = PhotoImage(file='./img/button/chup.png')
        self.cap = Button(self.Screenshot, image=self.btnChup, command=self.receive_picture, bd=0) # Chụp ảnh
        self.cap.place(relx=0, rely=0.88)

        self.btnSave = PhotoImage(file='./img/button/luu.png')
        self.Save = Button(self.Screenshot, image=self.btnSave, command=self.save_picture, bd=0) # Lưu ảnh
        self.Save.place(relx=0.4532, rely=0.88)

        self.btnDSave = PhotoImage(file='./img/button/khongluu.png')
        self.DontSave = Button(self.Screenshot, image=self.btnDSave, command=self.dont_save_picture, bd=0) # Không lưu ảnh
        self.DontSave.place(relx=0.7531, rely=0.88)

    def receive_picture(self):
        try:
            self.client.sendall(bytes("screenCapture", "utf-8")) # Gửi ảnh
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối") # Thất bại báo lỗi
            self.Screenshot.destroy()

        self.file = open("picture.png", 'wb') # Mở ảnh để viết ?
        self.data = self.client.recv(20126062)
        self.file.write(self.data)
        self.img = ImageTk.PhotoImage(Image.open("picture.png")) # Mở ảnh để xem
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.file.close()

    def save_picture(self):
        self.myScreenShot = open("picture.png", 'rb') # Mở ảnh để đọc
        self.data = self.myScreenShot.read()
        self.fname = filedialog.asksaveasfilename(title=u'Save file', filetypes=[("PNG", ".png")])
        self.myScreenShot.close()

        self.file = open(str(self.fname) + '.png', 'wb') # Mở ảnh để viết
        self.file.write(self.data)
        self.file.close()
        os.remove("picture.png") # Xóa ảnh trong bộ nhớ
        self.Screenshot.destroy()

    def dont_save_picture(self):
        os.remove("picture.png")
        self.Screenshot.destroy()

