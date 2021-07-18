from search import search_video
import tkinter
import tkinter.ttk as ttk
from extractor import Infos
import threading
from canvas import Canvas


class Interface(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.image_button = tkinter.PhotoImage(file="imgs/search (1).png")
        self.image_button_download = tkinter.PhotoImage(file="imgs/download (1).png")
        super().geometry("720x480")
        self.all_canvas = None
        style = ttk.Style()
        style.configure(
            "blue.Horizontal.TProgressbar",
            background="#32a852",
            bd=0,
            highlightthickness=0,
            relief=tkinter.FLAT,
        )
        self.title("telechargeur de musique akitologique")
        self.config(bd=0, bg="#14135b")
        self.minsize(720, 480)
        self.frame = tkinter.Frame(self, bg="#14135b")
        self.progress_frame = tkinter.Frame(self, bg="#14135b")
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            length=250,
            mode="determinate",
            orient="horizontal",
            style="blue.Horizontal.TProgressbar",
        )
        self.indication_label = tkinter.Label(
            self,
            text="appuyez pour chercher ....",
            bg="#14135b",
            fg="white",
            font=("arial", 20),
        )
        self.entry = tkinter.Entry(
            self.frame,
            bg="#22229a",
            font=("arial", 18),
            width=52,
            justify="center",
            bd=1,
            fg="white",
            relief=tkinter.FLAT,
            highlightthickness=0,
        )
        self.entry.pack(side=tkinter.LEFT)
        self.progress_label = tkinter.Label(
            self.progress_frame,
            text="aucun telechargement en cours",
            bg="#14135b",
            fg="white",
            font=("arial", 12),
        )
        self.progress_label.pack(side=tkinter.RIGHT, padx=20)
        self.search_button = tkinter.Button(
            self.frame,
            image=self.image_button,
            width=30,
            height=30,
            borderwidth=0,
            bg="#22229a",
            command=self.download,
            highlightthickness=0,
            activebackground="#282885",
        )
        self.search_button.pack(side=tkinter.RIGHT)
        self.frame.pack(side=tkinter.TOP)
        self.canvas_frame = tkinter.Frame(self, bg="#14135b")
        self.indication_label.pack(side=tkinter.TOP)
        self.progress_bar.pack(side=tkinter.LEFT)
        self.progress_frame.pack(side=tkinter.TOP)
        self.canvas_frame.pack(expand=True)
        self.play_image = tkinter.PhotoImage(file="imgs/play (1).png")

    def run(self):
        self.mainloop()

    def creat_canvas(self, name):
        infos = search_video(name, 6)
        all_canvas = []
        for i in range(5):
            try:
                all_canvas.append(
                    Canvas(self, self.canvas_frame, 720, 60, Infos(infos, i))
                )
            except IndexError:
                break
        if self.all_canvas:
            for i in self.all_canvas:
                i.destroy()
        self.all_canvas = all_canvas
        for canvas in self.all_canvas[::-1]:
            canvas.draw()
        self.indication_label["text"] = "appuyez pour chercher ...."
        self.search_button["state"] = tkinter.NORMAL

    def search(self):
        self.search_button["state"] = tkinter.DISABLED
        name = self.entry.get()
        if name.strip():
            self.indication_label["text"] = "en train de rechercher patientez svp ..."
            self.creat_canvas(name)
        else:
            self.entry.insert(0, "impossible to search")
        self.entry.delete(0, tkinter.END)
        raise NameError()

    def download(self):
        thread1 = threading.Thread(target=self.search)
        try:
            thread1.start()
        except NameError:
            pass


if __name__ == "__main__":
    interface = Interface()
    interface.run()
