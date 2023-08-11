import os
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
from PIL import Image


def screenCapture(self, client):
    self.Screenshot = Toplevel()					# Tạo 1 hộp thoại mới
    self.Screenshot.title("ScreenShot")			# Đặt tiêu đề cho hộp thoại
    self.Screenshot.resizable(width=False, height=False)
    self.Screenshot.iconbitmap('./img/button/remoteIcon.ico')
    # Đặt màu nền cho hộp thoại
    self.Screenshot.configure(bg="#C0C0C0", width=1090, height=610)
    # Hàm nhận ảnh từ server trả về

    def ReceivePicture():
        try:
            # Gửi thông điệp "screenCapture" đến server
            client.sendall(bytes("screenCapture", "utf-8"))
        except:
            # Nếu lỗi kết nối thì thông báo lỗi
            messagebox.showinfo("Error !!!", "Lỗi kết nối")
            self.Screenshot.destroy()							# Sau đó, đóng hộp thoại Screenshot lại

        self.file = open("picture.png", 'wb')					# Tạo file ảnh mới
        self.data = client.recv(20126062)						# Nhận dữ liệu từ server
        self.file.write(self.data)								# Ghi dữ liệu vào file ảnh
        self.img = ImageTk.PhotoImage(Image.open(
            "picture.png"))  # Tạo ảnh từ file ảnh
        self.canvas.create_image(
            0, 0, anchor=NW, image=self.img)  # Vẽ ảnh lên canvas
        self.file.close()											# Đóng file ảnh
        # Hàm lưu ảnh

    def SavePicture():
        self.myScreenShot = open("picture.png", 'rb')				# Tạo file ảnh mới
        self.data = self.myScreenShot.read()						# Đọc dữ liệu từ file ảnh
        self.fname = filedialog.asksaveasfilename(title=u'Save file', filetypes=[
                                                  ("PNG", ".png")])		# Đặt tên file ảnh và nhấn Save
        self.myScreenShot.close()						# Đóng file ảnh

        self.file = open(str(self.fname) + '.png', 'wb')			# Tạo file ảnh mới
        self.file.write(self.data)								# Ghi dữ liệu vào file ảnh
        self.file.close()										# Đóng file ảnh
        os.remove("picture.png") 								# Xóa file ảnh cũ
        self.Screenshot.destroy()								# Đóng hộp thoại Screenshot lại
        # Hàm không lưu ảnh

    def DontSavePicture():
        os.remove("picture.png")
        self.Screenshot.destroy()

        # Tạo canvas chứa ảnh đã chụp
    self.canvas = Canvas(self.Screenshot, bg="white",
                         width=1084, height=531) 	# Tạo canvas mới
    self.canvas.place(relx=0, rely=0)   		# Vẽ ảnh chụp màn hình lên canvas
    # Tạo button Chụp ảnh
    # Đặt hình ảnh
    self.btnChup = PhotoImage(file='./img/button/chup.png')
    self.cap = Button(self.Screenshot, image=self.btnChup,
                      command=ReceivePicture, bd=0)  # Nút chụp hình
    self.cap.place(relx=0, rely=0.88)
    # Tạo button Lưu ảnh
    # Đặt hình ảnh
    self.btnSave = PhotoImage(file='./img/button/luu.png')
    self.Save = Button(self.Screenshot, image=self.btnSave,
                       command=SavePicture, bd=0)  # Nút luu ảnh
    self.Save.place(relx=0.4532, rely=0.88)
    # Tạo button Không lưu ảnh
    # Đặt hình ảnh
    self.btnDSave = PhotoImage(file='./img/button/khongluu.png')
    self.DontSave = Button(self.Screenshot, image=self.btnDSave,
                           command=DontSavePicture, bd=0)  # Nút luu ảnh
    self.DontSave.place(relx=0.7531, rely=0.88)
    self.Screenshot.mainloop()
    os.remove("picture.png")
