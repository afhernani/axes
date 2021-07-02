#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter import Variable, ttk
from tkinter.constants import LEFT, RIGHT, TRUE
from tkinter.messagebox import showerror, showinfo
from tkinter import filedialog as fd
import cv2
import PIL.Image, PIL.ImageTk
import time
import datetime
import logging
import imageio


__author__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'modcv - opencv'
__version__ = '0'

__all__ = ('MyVideoCapture')

logging.basicConfig(level=logging.DEBUG)


class MyVideoCapture:
    
    '''video_source: str
    vid: cv2.VideoCapture
    width: int
    height: int
    n_frames: int
    fps: float
    seconds: float
    time: str'''
    
    def __init__(self, video_source=None):
        self.poss = 0.0 # posicion en milisegundos
        self.frames = []
        try:
            self.set_video(video_source)
        except Exception as e:
            logging.warning(str(e.args))
        
    def set_info(self):
        if self.vid.isOpened():
            self.n_frames = self.vid.get(cv2.CAP_PROP_FRAME_COUNT)
            self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))
            self.seconds = round((self.n_frames / self.fps), 3)
            self.time = str(datetime.timedelta(seconds=self.seconds))
    
    def set_dimension(self):
        if self.vid.isOpened():
            # Get video source width and height
            self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def set_video(self, video_source):
        self.video_source=None if video_source is None else video_source
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError(f"Unable to open video source: {video_source}")
        self.set_dimension()
        self.set_info()

    def set_poss(self, sec):
        '''set possition in secons'''
        self.vid.set(cv2.CAP_PROP_POS_MSEC,sec*1000)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            self.poss = self.vid.get(cv2.CAP_PROP_POS_MSEC)
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                logging.info(f'valor ret: {ret}')
                self.set_poss(0) # posicionamos al principio
                return (ret, None)
        else:
            raise ValueError(f"not open video source: {self.video_source}")

    def _get_frame_sec(self, sec):
        '''devuelve true/false, true, guarda imagen de la secuencia sec,
         en segundos.'''
        self.vid.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        ret, frame = self.vid.read()
        if ret:
            self.frames.append(frame)
            # cv2.imwrite("image"+str(count)+".jpg", image)     # save frame as JPG file
            return ret
        else:
            return False

    def save_gif_file(self, namefile="smiling", duration=0.8):
        logging.info("Extract n frames from video")
        self._get_frames_from_video()
        logging.info("Saving GIF file")
        if not namefile.endswith(('.gif')):
            namefile += '_nfx_.gif'
        with imageio.get_writer(namefile, mode="I",duration=duration) as writer:
            for idx, frame in enumerate(self.frames):
                logging.info(f"Adding frame to GIF file:  {idx + 1}")
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                writer.append_data(rgb_frame)

    def _get_frames_from_video(self, nft=20):
        rate_sec = round((self.seconds / (nft + 1)), 3)
        sec = rate_sec
        success = self._get_frame_sec(sec)
        while success:
            sec += rate_sec
            sec = round(sec, 2)
            success = self._get_frame_sec(sec)

    def __del__(self):
        ''' release de video soruce when de object is destroy'''
        # if self.vid.isOpened():
        self.vid.release()


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window_title = window_title
        self.window.title(window_title)
        self.video_source = video_source
        self.stop = False
        self.v_time = tk.DoubleVar()
        self.all_time = tk.DoubleVar()
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        if not self.vid.vid.isOpened():
            showerror(title="Aviso", message=f"No se pudo abrir la fuente {self.video_source}")
            exit(0)
        # Create a canvas that can fit the above video source size
        self.all_time.set(self.vid.seconds)
        self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Frame contenedor
        self.frame = tk.Frame(self.window)

        # Button that lets the user take a snapshot
        self.btn_snapshot=tk.Button(self.frame, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(side=tk.LEFT) #anchor=tkinter.CENTER, expand=True)

        # Button that lets us to create a gif file.
        self.btn_gif=tk.Button(self.frame, text="Gif", command=self.gifshow)
        self.btn_gif.pack(side=tk.LEFT)
        # stop button
        self.btn_stop = tk.Button(self.frame, text='II', command=self.stopshow)
        self.btn_stop.pack(side=tk.LEFT)

        # slider.
        options={'tickinterval': 0 , 'showvalue': True, 'resolution':0.1}
        self.slider = tk.Scale(self.frame, from_=0,
                                to=self.all_time.get(), 
                                orient='horizontal',
                                command=self.slider_changed,
                                variable=self.v_time,
                                **options
                                 )
        self.slider.pack(side=LEFT, expand=True, fill=tk.BOTH)

        # Button that let us to open another video file.
        self.btn_open=tk.Button(self.frame, text="Open", command=self.openshow)
        self.btn_open.pack(side=tk.RIGHT)
        # Etiqueta time
        self.lb_time =tk.Label(self.frame, text="...", width=8)
        self.lb_time.pack(side=tk.RIGHT)

        # pack frame
        self.frame.pack(anchor=tk.CENTER, expand=TRUE, fill=tk.BOTH)

        # After it is called once, the update method will be automatically called every delay milliseconds
        logging.info(f"fps: {self.vid.fps}")
        self.window.bind('<Configure>', self.handle_resize)
        self.delay = 18
        self.update()

        self.window.mainloop()
    
    def handle_resize(self, ev):
        logging.info(f"resize: {self.window.geometry()}")
        logging.info(f"canvas: {self.canvas.winfo_height()}, {self.canvas.winfo_width()}")
        logging.info(f"frame: {self.frame.winfo_height()}, {self.frame.winfo_width()}")

    def slider_changed(self, value):
        logging.info(f'time: {str(self.v_time.get())}, value: {value}')
        logging.info(f"valor scale: {self.slider.get()}")
        valor = self.slider.get()
        self.vid.set_poss(valor)

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def stopshow(self):
        if self.btn_stop['text'] == 'II':
            self.btn_stop['text'] = '>>'
            self.stop=True
        elif self.btn_stop['text'] == '>>':
            self.btn_stop['text'] = 'II'
            self.stop=False
            self.window.after(self.delay, self.update)

    def gifshow(self):
        self.vid.save_gif_file(namefile=self.video_source)

    def openshow(self):
        filetypes = (
            ('text files', '*.mp4'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
                        title='Open a file',
                        initialdir='.',
                        filetypes=filetypes
                        )
        if filename:
            logging.info(f"open file: {filename}")
            logging.info(f"before load, window {self.window.geometry()}")
            self.video_source = filename
            self.vid = MyVideoCapture(self.video_source)
            self.canvas.configure(width=self.vid.width, height=self.vid.height)
            self.all_time.set(self.vid.seconds)
            self.slider.configure(to=self.all_time.get())
            logging.info(f"new fps: {self.vid.fps}")
            # self.delay = int(self.vid.fps * 0.45)
            # logging.info(f"delay: {self.delay}")
            logging.info(f"window: {self.window.geometry()} ")

    def update(self):
        # Get a frame from the video source
        try:
            ret, frame = self.vid.get_frame()
            # self.window.title(self.window_title + ' :: '+ str(round((self.vid.poss / 1000), 2)))
            self.v_time.set(round((self.vid.poss / 1000), 3)) 
            self.lb_time['text'] = str(round(self.v_time.get(), 1))
        except:
            logging.debug("App update error ...")
            # salimos del loop ...
            return

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

        if self.stop:
            # salimos del loop
            return

        self.window.after(self.delay, self.update)


if __name__ == '__main__':
    # Create a window and pass it to the Application object
    App(tk.Tk(), "Tkinter and OpenCV", "Believer-Halo-560p.mp4")