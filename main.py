# This is a sample Python script.
import tkinter as tk
from PIL import ImageTk, Image

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_header()
        self.create_text_input()
        self.create_gallery()

    def create_text_input(self):
        self.input_frame = tk.Frame(root, width=100, height=100)
        self.input_frame.pack()
        # Text input
        text1 = tk.Text(self.input_frame, height=1, width=20, bg="gray", highlightthickness=0)
        # text1.grid(sticky="n")
        text1.pack(side="top")

        # Search button
        # btn = tk.Button(self, text="ค้นหา")
        # btn["command"] = self.search("test")
        # btn.pack(side="left")

    def search(self, text):
        print("u search: " + text)

    def create_sub_gallery(self, imagePath):
        origin = Image.open(imagePath)
        resized = origin.resize((100, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized)
        img = tk.Label(self.gallery_frame, image=photo)
        img.image = photo
        img.pack(side=tk.LEFT)

    def create_gallery(self):
        self.gallery_frame = tk.Frame(root,width=100, height=100)
        self.gallery_frame.pack()
        self.create_sub_gallery("img/test.gif")
        self.create_sub_gallery("img/test2.gif")
        self.create_sub_gallery("img/test.gif")
        self.create_sub_gallery("img/test2.gif")
        self.create_sub_gallery("img/test.gif")
        self.create_sub_gallery("img/test2.gif")
        self.create_sub_gallery("img/test.gif")
        self.create_sub_gallery("img/test2.gif")
        self.create_sub_gallery("img/test.gif")
        self.create_sub_gallery("img/test2.gif")
    def create_header(self):
        var = tk.StringVar()
        text_header = tk.Label(self, textvariable=var)
        text_header.config(height=2)
        text_header.pack(side="top")
        var.set("พิมพ์คำค้นหาที่ช่องด้านล่าง")


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

