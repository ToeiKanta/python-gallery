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
        # self.create_gallery()

    def create_text_input(self):

        # Text input
        text1 = tk.Text(root, height=1, width=30, bg="gray", highlightthickness=0)
        text1.pack(side="top")
        # Search button
        # btn = tk.Button(self, text="ค้นหา")
        # btn["command"] = self.search("test")
        # btn.pack(side="left")

    def search(self, text):
        print("u search: " + text)

    def create_gallery(self):
        photo = ImageTk.PhotoImage(Image.open("img/test2.gif"))
        img = tk.Label(self, image=photo)
        img.image = photo
        img.pack(side=tk.LEFT)

        text2 = tk.Text(root, height=20, width=50)
        scroll = tk.Scrollbar(root, command=text2.yview)
        text2.configure(yscrollcommand=scroll.set)
        text2.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
        text2.tag_configure('big', font=('Verdana', 20, 'bold'))
        text2.tag_configure('color',
                            foreground='#476042',
                            font=('Tempus Sans ITC', 12, 'bold'))
        text2.tag_bind('follow',
                       '<1>',
                       lambda e, t=text2: t.insert(tk.END, "Not now, maybe later!"))
        text2.insert(tk.END, '\nWilliam Shakespeare\n', 'big')
        quote = """
        To be, or not to be that is the question:
        Whether 'tis Nobler in the mind to suffer
        The Slings and Arrows of outrageous Fortune,
        Or to take Arms against a Sea of troubles,
        """
        text2.insert(tk.END, quote, 'color')
        text2.insert(tk.END, 'follow-up\n', 'follow')
        text2.pack(side=tk.LEFT)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

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

