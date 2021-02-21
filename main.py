import tkinter as tk
from PIL import ImageTk, Image
import os
import pyexiv2
from tkinter import ttk
import threading

## component สำหรับสร้าง TextBox ที่จะเรียก Event เมื่อมีการเปลี่ยนแปลงข้อความใน TextBox
class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result

## ตัวโปรแกรมหลัก
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        ## ตั้งค่าหน้าปัจจุบันของโปรแกรม
        self.current_page_index = 1
        ## ตั้งค่าจำนวนรูปที่แสดง ต่อ 1 แถว
        self.img_per_row = 5
        ## ตั้งค่าจำนวนแถวที่แสดงรูปภาพในแต่ละหน้าโปรแกรม
        self.img_row_count = 3
        ## เปิด-ปิดโหมดค้นรูปแบบอัตโนมัติ เมื่อเราแก้ไขข้อความในช่องค้นหา
        self.auto_search = False
        ## เก็บข้อความที่กรอกในช่องค้นหา
        self.input = ""
        ## ทำการสร้างหน้าต่างโปรแกรม
        self.master = master
        self.pack()
        self.create_row_item_selection()
        self.create_text_input_frame()
        self.create_page_pagination()
        self.create_gallery()

    ## สร้าง Frame สำหรับส่วนบนของโปรแกรม
    ## ชื่อเรื่อง ช่องค้นหา ปุ่มเปิด-ปิดโหมดค้นหาออโต้
    def create_text_input_frame(self):
        self.input_frame = tk.Frame(root, width=100, height=100)
        self.input_frame.pack(side="top")
        ## header lable
        var = tk.StringVar()
        text_header = tk.Label(self.input_frame, textvariable=var, height=2)
        text_header.pack(side="top")
        var.set("PLEASE ENTER IMAGE NAME BELOW")
        self.create_text_input()

    ## สร้าง TextBox ไว้เป็นช่องค้นหา และ
    def create_text_input(self):
        self.input_textbox_frame = tk.Frame(self.input_frame)
        self.input_textbox_frame.pack(side="top")
        ## สร้าง Text input สำหรับกรอกคำค้นหา
        self.input_textbox = CustomText(self.input_textbox_frame, height=1, width=20, font=("Helvetica", 19), bg="gray", highlightthickness=0)
        self.input_textbox.pack(side="left")
        if self.auto_search:
            self.input_textbox.bind("<<TextModified>>", self.search_img)
            self.input_textbox.bind("<Return>", self.reset_text) # เพื่อแก้บัค
        else:
            self.input_textbox.bind("<Return>", self.search_img_by_enter)
        ## สร้าง checkbox สำหรับ เปิด-ปิด โหมดค้นหาอัตโนมัติ
        if self.auto_search:
            text = "AUTO SEARCH: ON"
        else:
            text = "AUTO SEARCH: OFF"
        self.auto_label = tk.Label(self.input_textbox_frame, text=text, borderwidth=2, relief="raised", cursor="hand2", padx=2)
        self.auto_label.pack(side="right")
        ## เรียกใช้ฟังก์ชันเมื่อมีการคลิกซ้ายที่ ปุ่ม ค้นหาออโต้
        self.auto_label.bind("<Button-1>", self.toggleAutoSearch)

    ## ฟังชั่น Event Handler สำหรับปรับโหมดค้นหาออโต้
    def toggleAutoSearch(self, event):
        self.auto_search = not self.auto_search
        self.input_textbox_frame.destroy()
        self.create_text_input()

    ## สร้างปุ่มเปลี่ยนหน้าโปรแกรม prev -- next
    def create_page_pagination(self):
        paginationFrame = tk.Frame(root, pady=5)
        paginationFrame.pack()
        next_btn = tk.Label(paginationFrame, text="BACK", borderwidth=2, relief="raised", cursor="hand2")
        next_btn.bind("<Button-1>", self.backPage)
        next_btn.pack(side="left")
        self.current_page_label = tk.Label(paginationFrame, text=" - page " + str(self.current_page_index) + " - ")
        self.current_page_label.pack(side="left")
        next_btn = tk.Label(paginationFrame, text="NEXT", borderwidth=2, relief="raised", cursor="hand2")
        next_btn.bind("<Button-1>", self.nextPage)
        next_btn.pack(side="left")

    ## Event handler สำหรับไปหน้าถัดไป
    def nextPage(self,event):
        self.current_page_index += 1
        self.reload_gallery()

    ## Event handler สำหรับกลับไปหน้าก่อน
    def backPage(self, event):
        if self.current_page_index > 1:
            self.current_page_index -= 1
            self.reload_gallery()

    ## Event handler สำหรับเลือกจำนวนแถวที่แสดง จาก combobox
    def row_select_handle(self, event):
        self.img_row_count = int(event.widget.get())
        self.reload_gallery()

    ## Event handler สำหรับเลือกจำนวนรูปที่แสดงในแต่ละแถว จาก combobox
    def item_count_select_handle(self, event):
        self.img_per_row = int(event.widget.get())
        self.reload_gallery()

    ## สร้าง Frame สำหรับแสดง combobox เลือกจำนวนรูป และแถว ที่แสดงในโปรแกรม
    def create_row_item_selection(self):
        ## row count
        frame = tk.Frame(root,width=50)
        frame.pack()
        rowLabel = tk.Label(frame, text="Table dimension:")
        rowLabel.pack(side="left")
        comboExample = ttk.Combobox(frame, state="readonly", values=[1, 2, 3], width=3)
        comboExample.pack(side="left")
        comboExample.current(self.img_row_count-1)
        comboExample.bind("<<ComboboxSelected>>", self.row_select_handle)
        ## item per row
        rowLabel = tk.Label(frame,
                            text="X")
        rowLabel.pack(side="left")
        comboExample = ttk.Combobox(frame, state="readonly", values=[1, 2, 3, 4, 5, 6, 7, 8], width=3)
        comboExample.pack(side="left")
        comboExample.current(self.img_per_row-1)
        comboExample.bind("<<ComboboxSelected>>", self.item_count_select_handle)

    ## ฟังชันบันทึกข้อความในลงรูปภาพ
    def save_description(self, image_path, string):
        print("save: " + image_path + " :: " + string)
        img = pyexiv2.Image(image_path, encoding='utf-8')
        userdata = {'Xmp.dc.desciption' : string}
        img.modify_xmp(userdata)
        img.close()
        self.reload_gallery()

    ## ฟังชันบันทึกข้อความในลงรูปภาพ เมื่อกดปุ่ม 'บันทึก'
    def save_description_text_box(self, image_path, desc_text_component):
        string = desc_text_component.get("1.0", "end-1c")
        self.save_description(image_path, string)

    ## ฟังชันบันทึกข้อความในลงรูปภาพ เมื่อกดปุ่ม 'บันทึกและออก'
    def save_description_text_box_quit(self, image_path, desc_text_component, window):
        self.save_description_text_box(image_path, desc_text_component)
        window.destroy()

    ## อ่านข้อความจากรูป ที่เคยบันทึกไว้ และคืนค่าข้อความนั้น
    def read_description(self, image_path):
        img = pyexiv2.Image(image_path, encoding='utf-8')
        metadata = img.read_xmp()
        img.close()
        return metadata['Xmp.dc.desciption']

    ## ฟังชันล้างข้อความทั้งหมดในช่องค้นหารูป
    def reset_text(self, event):
        ## reset text input
        self.input_textbox.delete("1.0", "end")
        self.input_textbox.insert("1.0", "")
        self.input = ""

    ## Event handler สำหรับค้นหารูปจากข้อความในช่องค้นหา
    def search_img(self, event):
        self.input = event.widget.get("1.0", "end-1c")
        self.current_page_index = 1
        self.reload_gallery()

    ## Event handler สำหรับค้นหารูปจากข้อความในช่องค้นหา ด้วยการกด enter (จะล้างข้อความในช่องต้นหาหลังกดปุ่ม Enter)
    def search_img_by_enter(self, event):
        self.search_img(event)
        ## ล้างข้อความ
        self.input_textbox.delete("1.0", "end")
        self.input_textbox.insert("1.0", "")

    ## รีโหลดรูปภาพทั้งหมดในโปรแกรม
    def reload_gallery(self):
        ## for child in self.gallery_frame.winfo_children():
        ##     child.destroy()
        self.gallery_frame.destroy()
        self.create_gallery()
        self.current_page_label['text'] = " - page " + str(self.current_page_index) + " - "

    ## เปืดหน้าต่างโปรแกรม สำหรับดูรูปภาพขนาดใหญ่
    def go_full_image(self, full_image_path):
        ## create new window
        newWindow = tk.Toplevel(root)
        newWindow.title(full_image_path)
        newWindow.geometry("1200x700")
        ## show picture graph
        filename, file_extension = os.path.splitext(full_image_path)
        # '/path/to/somefile.ext'
        # >>> filename
        # '/path/to/somefile'
        # >> > file_extension
        # '.ext'
        full_image_graph_path = filename + "-graph" + file_extension
        ## resize picture if having graph
        pictureSize = (500,500)
        if (os.path.exists(full_image_graph_path)):
            pictureSize = (250, 250)
        ## picture
        origin = Image.open(full_image_path)
        resized = origin.resize(pictureSize, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized)
        img = tk.Label(newWindow, image=photo)
        img.image = photo
        img.pack(side="left")

        if (os.path.exists(full_image_graph_path)):
            origin = Image.open(full_image_graph_path)
            resized = origin.resize(pictureSize, Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(resized)
            img = tk.Label(newWindow, image=photo)
            img.image = photo
            img.pack(side="left")
        ## picture description
        right_frame = tk.Frame(newWindow, padx=3)
        right_frame.pack(side="left")
        ## image label
        temp_text = "Image Path: \n" + full_image_path + "\n\nImage Description:"
        if (os.path.exists(full_image_graph_path)):
            temp_text = "Image Path: \n" + full_image_path + "\n" + full_image_graph_path + "\n\nImage Description:"
        image_label = tk.Label(right_frame, text=temp_text, justify="left", font=("Courier", 12))
        image_label.pack(side="top",anchor="nw")
        ## description text area
        frameDesc = tk.Frame(right_frame)
        frameDesc.pack(fill="both")
        tableLayout = ttk.Notebook(frameDesc)
        # Tab 1
        tab1 = tk.Frame(tableLayout)
        tab1.pack(fill="both")
        desc = tk.Text(tab1, font=("Courier", 14))
        desc.insert(tk.INSERT, self.read_description(full_image_path))
        desc.pack(side="top")
        desc.focus_set()
        tableLayout.add(tab1,text="Description")
        tableLayout.pack(fill="both")
        # Tab 2
        tab1 = tk.Frame(tableLayout)
        tab1.pack(fill="both")
        for row in range(5):
            for column in range(6):
                label = tk.Label(tab1,text = "r:" + str(row) + "c:" + str(column),padx=3,pady=3,bg="black",fg="white")
                label.grid(row=row,column=column,sticky="nsew",padx=1,pady=1)
                tab1.grid_columnconfigure(column,weight=1)
        tableLayout.add(tab1, text="Excel")
        tableLayout.pack(fill="both")
        ## save button
        save_btn = tk.Label(right_frame,text="SAVE", borderwidth=2, relief="raised", cursor="hand2")
        save_btn.bind("<Button-1>", lambda e, full_image_path=full_image_path, desc=desc: self.save_description_text_box(full_image_path, desc))
        save_btn.pack(side="top", pady=2)
        ## save and quit button
        save_quit_btn = tk.Label(right_frame, text="SAVE AND QUIT", borderwidth=2, relief="raised", cursor="hand2")
        save_quit_btn.bind("<Button-1>", lambda e, full_image_path=full_image_path, desc=desc,newWindow=newWindow: self.save_description_text_box_quit(full_image_path, desc, newWindow))
        save_quit_btn.pack(side="top", pady=2)
        ## quit button
        quit_btn = tk.Label(right_frame, text="QUIT", borderwidth=2, relief="raised", cursor="hand2")
        quit_btn.bind("<Button-1>", lambda e, newWindow=newWindow: newWindow.destroy())
        quit_btn.pack(side="top", pady=2)

    ## แสดงรูปภาพแต่ละรูปใน Frame รูปแบบ ใน 1 หน้าของโปรแกรม
    def create_sub_gallery(self, frame, imagePath, imageName):
        frame = tk.Frame(frame)
        frame.pack(side="left", padx=5, pady=5) ## pack frame to gallery_frame
        ## picture name
        var = tk.StringVar()
        text_header = tk.Label(frame, textvariable=var)
        text_header.config(height=4)
        text_header.pack(side="bottom")
        try:
            desc = self.read_description(imagePath)
        except:
            self.save_description(imagePath, "default description")
            desc = self.read_description(imagePath)
        var.set(imageName + "\n" + desc[:30] + "...")
        ## picture
        origin = Image.open(imagePath)
        resized = origin.resize((100, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized)
        img = tk.Label(frame, image=photo)
        img.bind("<Button-1>", lambda e, imagePath=imagePath: self.go_full_image(imagePath))
        img.image = photo
        img.pack(side="top")

    ## สร้าง Frame Gallery สำหรับแสดงรูปภาพที่ค้นหาได้ทั้งหมด
    def create_gallery(self):
        self.gallery_frame = tk.Frame(root, width=100, height=100, highlightbackground="gray", highlightcolor="gray", highlightthickness=2 )
        self.gallery_frame.pack()
        dataPath = "./img"
        # print("=" + self.input + "=")
        start_i = (self.current_page_index-1) * (self.img_per_row * self.img_row_count)
        i = 0
        row = tk.Frame(self.gallery_frame)
        row.pack(side="top")
        for path, subdirs, files in os.walk(dataPath):
            for file in files:
                filename, file_extension = os.path.splitext(file)
                if (file.endswith(".gif") or file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg")) and not filename.endswith("-graph") and self.input.replace("\n", "") in file:
                    if i < start_i:
                        i += 1
                        continue
                    if(i % self.img_per_row == 0):
                        row = tk.Frame(self.gallery_frame)
                        row.pack(side="top")
                    i += 1
                    if i > (self.current_page_index) * (self.img_per_row * self.img_row_count):
                        break
                    thr = threading.Thread(target=self.create_sub_gallery(row, os.path.join(path, file), file))
                    thr.start()

## โปรแกรมหลัก
if __name__ == '__main__':
    root = tk.Tk()
    ## ขนาดโปรแกรม
    root.geometry('1200x700')
    ## ชื่อโปรแกรม
    root.title("Python Gallery")
    ## สร้างหน้าต่างโปรแกรมหลัก
    app = Application(root)
    app.mainloop()
