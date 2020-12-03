# This is a sample Python script.
import tkinter as tk
from PIL import ImageTk, Image
import os
import pyexiv2

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
        self.img_per_row = 2
        self.img_row_count = 3
        self.input = ""
        self.master = master
        self.pack()
        self.create_header()
        self.create_text_input()
        self.create_gallery()
        self.save_description("./img/test.gif")
        # print(self.read_description("./img/test.gif"))

    def create_text_input(self):
        self.input_frame = tk.Frame(root, width=100, height=100)
        self.input_frame.pack()
        # Text input
        self.input_textbox = CustomText(self.input_frame, height=1, width=20, bg="gray", highlightthickness=0)
        # text1.grid(sticky="n")
        self.input_textbox.pack(side="top")
        self.input_textbox.bind("<<TextModified>>", self.search_img)
        self.input_textbox.bind("<Return>", self.reset_text)

    def reset_text(self, event):
        # reset text input
        self.input_textbox.delete("1.0", "end")
        self.input_textbox.insert("1.0", "")
        self.input = ""

    def save_description(self, image_path):
        img = pyexiv2.Image(image_path, encoding='utf-8')
        userdata = {'Xmp.dc.desciption' : "ทดสอบ รายละเอียด"}
        img.modify_xmp(userdata)
        img.close()

    def read_description(self, image_path):
        img = pyexiv2.Image(image_path, encoding='utf-8')
        metadata = img.read_xmp()
        img.close()
        return metadata['Xmp.dc.desciption']

    def search_img(self, event):
        self.input = event.widget.get("1.0", "end-1c")
        self.gallery_frame.pack_forget()
        self.create_gallery()


    def create_sub_gallery(self,frame, imagePath, imageName):
        self.save_description(imagePath)
        frame = tk.Frame(frame)
        frame.pack(side="left", padx=20, pady=20) # pack frame to gallery_frame
        # picture
        origin = Image.open(imagePath)
        resized = origin.resize((100, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized)
        img = tk.Label(frame, image=photo)
        img.image = photo
        img.pack(side="top")
        # picture name
        var = tk.StringVar()
        text_header = tk.Label(frame, textvariable=var)
        text_header.config(height=3)
        text_header.pack(side="bottom")
        var.set(imageName + "\n" + self.read_description(imagePath))


    def create_gallery(self):
        self.gallery_frame = tk.Frame(root, width=100, height=100)
        self.gallery_frame.pack()
        dataPath = "./img"
        print("=" + self.input + "=")
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

    def create_header(self):
        var = tk.StringVar()
        text_header = tk.Label(self, textvariable=var)
        text_header.config(height=2)
        text_header.pack(side="top")
        var.set("PLEASE ENTER IMAGE NAME")


    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

if __name__ == '__main__':
    root = tk.Tk()
    # app = tk.Frame(root, width=100, height=100, background="bisque")
    app = Application(root)
    app.mainloop()

