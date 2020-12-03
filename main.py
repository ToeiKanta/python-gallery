# This is a sample Python script.
import tkinter as tk
from PIL import ImageTk, Image
import os
import pyexiv2
from tkinter import ttk

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

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_page_index = 1
        self.img_per_row = 5
        self.img_row_count = 3
        self.input = ""
        self.master = master
        self.pack()
        self.create_row_item_selection()
        self.create_text_input()
        self.create_page_pagination()
        self.create_gallery()

    def create_text_input(self):
        self.input_frame = tk.Frame(root, width=100, height=100)
        self.input_frame.pack()
        # header lable
        var = tk.StringVar()
        text_header = tk.Label(self.input_frame, textvariable=var, height=2)
        text_header.pack(side="top")
        var.set("PLEASE ENTER IMAGE NAME BELOW")
        # Text input
        self.input_textbox = tk.Text(self.input_frame, height=1, width=20, font=("Helvetica", 19), bg="gray", highlightthickness=0)
        # text1.grid(sticky="n")
        self.input_textbox.pack(side="top")
        self.input_textbox.bind("<<TextModified>>", self.search_img)
        self.input_textbox.bind("<Return>", self.reset_text)

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


    def nextPage(self,event):
        self.current_page_index += 1
        self.reload_gallery()

    def backPage(self, event):
        if self.current_page_index > 1:
            self.current_page_index -= 1
            self.reload_gallery()

    def row_select_handle(self, event):
        self.img_row_count = int(event.widget.get())
        self.reload_gallery()

    def item_count_select_handle(self, event):
        self.img_per_row = int(event.widget.get())
        self.reload_gallery()

    def create_row_item_selection(self):
        # row count
        frame = tk.Frame(root,width=50)
        frame.pack()
        rowLabel = tk.Label(frame, text="Table dimension:")
        rowLabel.pack(side="left")
        comboExample = ttk.Combobox(frame, state="readonly", values=[1, 2, 3, 4], width=3)
        comboExample.pack(side="left")
        comboExample.current(self.img_row_count-1)
        comboExample.bind("<<ComboboxSelected>>", self.row_select_handle)
        # item per row
        rowLabel = tk.Label(frame,
                            text="X")
        rowLabel.pack(side="left")
        comboExample = ttk.Combobox(frame, state="readonly", values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], width=3)
        comboExample.pack(side="left")
        comboExample.current(self.img_per_row-1)
        comboExample.bind("<<ComboboxSelected>>", self.item_count_select_handle)

    def reset_text(self, event):
        # reset text input
        self.input_textbox.delete("1.0", "end")
        self.input_textbox.insert("1.0", "")
        self.input = ""

    def save_description(self, image_path, string):
        print("save: " + image_path + " :: " + string)
        img = pyexiv2.Image(image_path, encoding='utf-8')
        userdata = {'Xmp.dc.desciption' : string}
        img.modify_xmp(userdata)
        img.close()
        self.reload_gallery()

    def save_description_text_box(self, image_path, desc_text_component):
        string = desc_text_component.get("1.0", "end-1c")
        self.save_description(image_path, string)

    def save_description_text_box_quit(self, image_path, desc_text_component, window):
        self.save_description_text_box(image_path, desc_text_component)
        window.destroy()

    def read_description(self, image_path):
        img = pyexiv2.Image(image_path, encoding='utf-8')
        metadata = img.read_xmp()
        img.close()
        return metadata['Xmp.dc.desciption']

    def search_img(self, event):
        self.input = event.widget.get("1.0", "end-1c")
        self.current_page_index = 1
        self.reload_gallery()

    def reload_gallery(self):
        # for child in self.gallery_frame.winfo_children():
        #     child.destroy()
        self.gallery_frame.destroy()
        self.create_gallery()
        self.current_page_label['text'] = " - page " + str(self.current_page_index) + " - "

    def go_full_image(self, full_image_path):
        # create new window
        newWindow = tk.Toplevel(root)
        newWindow.title(full_image_path)
        newWindow.geometry("700x500")
        # picture
        origin = Image.open(full_image_path)
        resized = origin.resize((500, 500), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized)
        img = tk.Label(newWindow, image=photo)
        img.image = photo
        img.pack(side="left")
        # picture description
        right_frame = tk.Frame(newWindow, padx=3)
        right_frame.pack(side="left")
        # image label
        temp_text = "Image Path: \n" + full_image_path + "\n\nImage Description:"
        image_label = tk.Label(right_frame, text=temp_text, justify="left", font=("Courier", 12))
        image_label.pack(side="top",anchor="nw")
        # description text area
        desc = CustomText(right_frame, font=("Courier", 14))
        desc.insert(tk.INSERT, self.read_description(full_image_path))
        desc.pack(side="top")
        desc.focus_set()
        # save button
        save_btn = tk.Label(right_frame,text="SAVE", borderwidth=2, relief="raised", cursor="hand2")
        save_btn.bind("<Button-1>", lambda e, full_image_path=full_image_path, desc=desc: self.save_description_text_box(full_image_path, desc))
        save_btn.pack(side="top", pady=2)
        # save and quit button
        save_quit_btn = tk.Label(right_frame, text="SAVE AND QUIT", borderwidth=2, relief="raised", cursor="hand2")
        save_quit_btn.bind("<Button-1>", lambda e, full_image_path=full_image_path, desc=desc,newWindow=newWindow: self.save_description_text_box_quit(full_image_path, desc, newWindow))
        save_quit_btn.pack(side="top", pady=2)
        # quit button
        quit_btn = tk.Label(right_frame, text="QUIT", borderwidth=2, relief="raised", cursor="hand2")
        quit_btn.bind("<Button-1>", lambda e, newWindow=newWindow: newWindow.destroy())
        quit_btn.pack(side="top", pady=2)

    def create_sub_gallery(self,frame, imagePath, imageName):
        frame = tk.Frame(frame)
        frame.pack(side="left", padx=5, pady=5) # pack frame to gallery_frame
        # picture
        origin = Image.open(imagePath)
        resized = origin.resize((100, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized)
        img = tk.Label(frame, image=photo)
        img.bind("<Button-1>", lambda e, imagePath=imagePath: self.go_full_image(imagePath))
        img.image = photo
        img.pack(side="top")
        # picture name
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


    def create_gallery(self):
        self.gallery_frame = tk.Frame(root, width=100, height=100)
        self.gallery_frame.pack()
        dataPath = "./img"
        # print("=" + self.input + "=")
        start_i = (self.current_page_index-1) * (self.img_per_row * self.img_row_count)
        i = 0
        row = tk.Frame(self.gallery_frame)
        row.pack(side="top")
        for file in os.listdir(dataPath):
            if (file.endswith(".gif") or file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg")) and self.input.replace("\n", "") in file:
                if i < start_i:
                    i += 1
                    continue
                if(i % self.img_per_row == 0):
                    row = tk.Frame(self.gallery_frame)
                    row.pack(side="top")
                i += 1
                if i > (self.current_page_index) * (self.img_per_row * self.img_row_count):
                    break
                self.create_sub_gallery(row, os.path.join(dataPath, file), file)

if __name__ == '__main__':
    root = tk.Tk()
    # root.geometry('500x800')
    root.title("Python Gallery")
    app = Application(root)
    app.mainloop()
