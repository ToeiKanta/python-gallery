# This is a sample Python script.
import tkinter as tk
from PIL import ImageTk, Image
import os

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
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
        self.input = ""
        self.master = master
        self.pack()
        self.create_header()
        self.create_text_input()
        self.create_gallery()

    def create_text_input(self):
        self.input_frame = tk.Frame(root, width=100, height=100)
        self.input_frame.pack()
        # Text input
        self.input_text = CustomText(self.input_frame, height=1, width=20, bg="gray", highlightthickness=0)
        # text1.grid(sticky="n")
        self.input_text.pack(side="top")
        self.input_text.bind("<<TextModified>>", self.search)

    def search(self, event):
        self.input = event.widget.get("1.0", "end-1c")
        self.gallery_frame.pack_forget()
        self.create_gallery()

    def create_sub_gallery(self, imagePath, imageName):
        frame = tk.Frame(self.gallery_frame)
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
        text_header.config(height=1)
        text_header.pack(side="bottom")
        var.set(imageName)

    def create_gallery(self):
        self.gallery_frame = tk.Frame(root,width=100, height=100)
        self.gallery_frame.pack()
        dataPath = "./img"
        for file in os.listdir(dataPath):
            if (file.endswith(".gif") or file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"))\
                    and self.input in file:
                self.create_sub_gallery(os.path.join(dataPath, file),file)

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

