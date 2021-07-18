import tkinter
from extractor import Extractor, Infos
import io
import requests
from PIL import Image, ImageTk
import tkinter.filedialog as dial
from webbrowser import open_new
import threading


class Canvas(tkinter.Canvas):
    def __init__(self, master, frame, width, height, infos: Infos):
        super().__init__(
            frame,
            width=width - 2,
            height=height,
            background="#191970",
            highlightcolor="#393984",
            highlightthickness=1,
        )
        self.infos = infos
        self.download_link = self.infos.download_url
        self._master = master
        self.image, self.image_size = self.convert_to_image_file(
            self.infos.thumbnail, 60
        )
        self.frame = tkinter.Frame(self, bg="#191970", bd=0)
        self.start_download_button = tkinter.Button(
            self.frame,
            image=self._master.image_button_download,
            width=30,
            height=30,
            borderwidth=0,
            bg="#191970",
            relief=tkinter.FLAT,
            highlightthickness=0,
            activebackground="#1f1f6b",
            command=self.download,
        )
        self.start_download_button.pack(side=tkinter.RIGHT)
        self.test_button = tkinter.Button(
            self.frame,
            image=self._master.play_image,
            width=30,
            height=30,
            borderwidth=0,
            bg="#191970",
            relief=tkinter.FLAT,
            highlightthickness=0,
            activebackground="#1f1f6b",
            command=self.play,
        )
        self.bytes_tests = Extractor.extract_first_of_music(
            self.download_link, io.BytesIO()
        )
        self.test_button.pack(side=tkinter.LEFT, padx=10)
        self.done = 0
        self.display()
        self.downloader = None

    def convert_to_image_file(self, thumbnail_url, height):
        rps = requests.get(thumbnail_url, stream=True)
        print(thumbnail_url)
        if rps.ok:
            image = Image.open(io.BytesIO(rps.content))
            pourcent = height / image.size[1]
            transformed_width = image.size[0] * pourcent
            image = image.resize((int(transformed_width), height), Image.ANTIALIAS)
            return (ImageTk.PhotoImage(image), image.size)
        else:
            raise Exception("impossible de charger les images thumbnails")

    def display(self):
        size = self.image_size
        self.create_image(size[0] // 2, size[1] // 2, image=self.image)
        self.create_line(size[0] + 10, 0, size[0] + 10, size[1])
        self.create_line(size[0] + 5, 1, size[0] + 15, 1)
        self.create_line(size[0] + 5, size[1], size[0] + 15, size[1])
        text_place = size[0] + 20
        y = 0
        for mini_info, description in self.infos.all_infos_list:
            self.create_text(
                text_place,
                y,
                font=("arial", 10),
                text=f"{description} {mini_info}",
                anchor=tkinter.NW,
                fill="white",
            )
            y += 20
        self.frame.place(x=620, y=15)
        self.update()

    def draw(self):
        self.pack(pady=6, side=tkinter.BOTTOM)

    def start_download(self):
        if self.downloader is None:
            filetypes = (("musics", "*.webm"), ("All files", "*.*"))
            name = dial.asksaveasfilename(
                filetypes=filetypes,
                title="chose the name of the file",
                initialfile=self.infos.title.replace("/", " "),
            )
            if not name:
                raise NameError()
            self.downloader = Extractor.download_music(
                self.download_link, name, self.infos.size, write=False, pourcent=100
            )
        for canvas in self._master.all_canvas:
            canvas.start_download_button["state"] = tkinter.DISABLED
        while True:
            try:
                value = next(self.downloader)
                self._master.progress_bar["value"] = value
                self.done = value
                title = (
                    self.infos.title
                    if len(self.infos.title) <= 20
                    else f"{self.infos.title[:20]} ..."
                )
                self._master.progress_label[
                    "text"
                ] = f"{title} is downloading pleas wait ..."
            except StopIteration:
                print("telechargement fini ...")
                self._master.progress_label["text"] = "Teléchargement fini"
                self._master.progress_bar["value"] = 0
                self.downloader = None
                for canvas in self._master.all_canvas:
                    canvas.start_download_button["state"] = tkinter.NORMAL
                raise NameError()

    def play(self):
        open_new(self.download_link)

    def download(self):
        thread1 = threading.Thread(target=self.start_download)
        try:
            thread1.start()
        except NameError:
            pass
