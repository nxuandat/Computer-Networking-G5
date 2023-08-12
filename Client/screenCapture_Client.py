import os
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image


class ScreenCapture:   # Hàm dùng để chụp màn hình
    def __init__(self, client):
        self.client = client
        self.Screenshot = Toplevel()    # Tạo 1 cửa sổ
        self.Screenshot.title("ScreenShot")  # Tên cửa sổ
        self.Screenshot.resizable(width=False, height=False) # Ngăn việc chỉnh kích thước cửa sổ
        self.Screenshot.iconbitmap('./img/button/remoteIcon.ico') # Icon button
        self.Screenshot.configure(bg="#C0C0C0", width=1090, height=610) # Cài đặt kích thước cửa sổ

        self.canvas = Canvas(self.Screenshot, bg="white", width=1084, height=531)   # Tạo khung ảnh
        self.canvas.place(relx=0, rely=0)   # Tọa độ khung ảnh (x=0,y=0)

        self.btnChup = PhotoImage(file='./img/button/chup.png') # Button cho chụp
        self.cap = Button(self.Screenshot, image=self.btnChup, command=self.receive_picture, bd=0) # Chụp ảnh
        self.cap.place(relx=0, rely=0.88) # Tọa độ button

        self.btnSave = PhotoImage(file='./img/button/luu.png') # Button lưu ảnh
        self.Save = Button(self.Screenshot, image=self.btnSave, command=self.save_picture, bd=0) # Lưu ảnh
        self.Save.place(relx=0.4532, rely=0.88) # Tọa độ button 

        self.btnDSave = PhotoImage(file='./img/button/khongluu.png') # Button không lưu ảnh
        self.DontSave = Button(self.Screenshot, image=self.btnDSave, command=self.dont_save_picture, bd=0) # Không lưu ảnh
        self.DontSave.place(relx=0.7531, rely=0.88) # Tọa độ button

    def receive_picture(self):      # Hàm để chương trình nhận ảnh
        try:
            self.client.sendall(bytes("screenCapture", "utf-8")) # Gửi ảnh
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối") # Thất bại báo lỗi
            self.Screenshot.destroy() # Hủy ảnh

        self.file = open("picture.png", 'wb') # Mở ảnh rỗng để viết byte
        self.data = self.client.recv(20126062) # Truyền dữ liệu byte từ client theo socket 20126062
        self.file.write(self.data) # Viết vào ảnh dữ liệu 
        self.img = ImageTk.PhotoImage(Image.open("picture.png")) # Mở ảnh để xem
        self.canvas.create_image(0, 0, anchor=NW, image=self.img) # Toa độ ảnh
        self.file.close() # Đóng ảnh để ngừng viết

    def save_picture(self): # Hàm để lưu ảnh
        self.myScreenShot = open("picture.png", 'rb') # Mở ảnh để đọc binary
        self.data = self.myScreenShot.read() # Lưu dữ liệu ảnh vào data
        self.fname = filedialog.asksaveasfilename(title=u'Save file', filetypes=[("PNG", ".png")]) # Mở cửa sổ để chọn chỗ lưu ảnh và tên ảnh
        self.myScreenShot.close() # Đóng ảnh để ngừng đọc

        self.file = open(str(self.fname) + '.png', 'wb') # Mở ảnh để viết
        self.file.write(self.data) # Viết vào ảnh dữ liệu 
        self.file.close() # Đóng ảnh để ngừng viết 
        os.remove("picture.png") # Xóa ảnh trong bộ nhớ (bộ nhớ tạm thời) 
        self.Screenshot.destroy() # Đóng cửa sổ lưu ảnh

    def dont_save_picture(self):  # Hàm để xóa ảnh
        os.remove("picture.png") # Xóa ảnh trong bộ nhớ (bộ nhớ tạm thời)
        self.Screenshot.destroy() # Đóng cửa sổ lưu ảnh

