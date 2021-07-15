#!/usr/bin/env python3
# _*_ coding:UTF-8 _*_

import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os, sys, subprocess
from threading import Thread
try:
    from modcv import MyVideoCapture
    from ToolTip import createToolTip
    from tooltipmenu import createToolTipMenu
    from windialog import WindowCopyTo, ToolFile, OpenDialogRename
    from imagetrans import Imagetrans
    from photos import Photos
except ImportError:
    from .modcv import MyVideoCapture
    from .ToolTip import createToolTip
    from .tooltipmenu import createToolTipMenu
    from .windialog import WindowCopyTo, ToolFile, OpenDialogRename
    from .imagetrans import Imagetrans
    from .photos import Photos

import logging

__author__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'axe - spritepane'
__version__ = '1.8.x'

__all__=('SpritePane')

logging.basicConfig(level=logging.DEBUG)


class SpritePane(tk.Frame):

    def __init__(self, parent, url=None, timer=None, *args, **kargs):
        
        super().__init__(parent, *args, **kargs)
        self.parent = parent
        self.url = '' if url is None else os.path.abspath(url) # path viedo
        self.ni = 32 # num de imagenes a extaer.
        self.timer = 21 if timer is None else timer
        # ---
        self.width = kargs.get('width', 300)
        self.height = kargs.get('height', 220)
        self.size =(self.width, self.height)
        # ----
        if self.url.upper().endswith(('.MP4', '.AVI', '.FLV', '.GIF', '.MPG', '.TS', '.WEBM', '.MOV', '.MKV')):
            self.graphics = MyVideoCapture(self.url, thumb=(self.width, self.height))
        else:
            raise ValueError(f"Unable to open video source: {self.url}")

        # --- duracion y creacion de createtooltip
        try:
            text = self.graphics.time
            createToolTip(self, text)
            self.ph_ico = Photos()
        except Exception as e:
            logging.warning(str(e.args))
            return
        #-----

        # TODO: Creamos menu
        self.menu = tk.Menu(self, tearoff=False)
        self.menu.add_command(label="move ...", image=self.ph_ico._move, compound="left", command=self.move)
        self.menu.add_command(label="copy ...", image=self.ph_ico._copy, compound="left", command=self.copy)
        self.menu.add_command(label="rename ...", image=self.ph_ico._rename, compound="left", command=self.rename)
        self.menu.add_separator()
        self.menu.add_command(label="remove ...", image=self.ph_ico._delete, compound="left", command=self.remove)
        createToolTipMenu(self, self.menu)
        # TODO: FIN MENU

        # -- TODO: extraemos imagen:
        self.f_interval = round((self.graphics.seconds / (self.ni + 1)), 2)
        self.f_way = self.f_interval
        # self.graphics.set_poss(self.f_interval)
        # self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.graphics.get_frame()[1]))
        self.photo = self.graphics.photo
        # -- TODO: FIN EXTRAER 1A IMAGEN
        
        # TODO: creamos canvas
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="yellow")
        self.canvas.pack()
        self.image = self.canvas.create_image(self.width/2, self.height/2, image=self.photo)
        self.canvas.bind('<Enter>', self.enter)
        self.canvas.bind('<Leave>', self.leave)
        self.canvas.bind('<Double-Button-1>', self.double_click_canvas)
        self.canvas.bind('<Button-3>', self.my_popup) # make menu
        self.animating = True
        # self.animate(0)

    # actuaciones de menu
    def my_popup(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def move(self):
        logging.info(f'move ->, {self.url}')
        new_url = tk.StringVar(value='None')
        url = tk.StringVar(value=self.url)
        to_ = tk.StringVar(value=os.path.dirname(self.url))
        if os.path.isfile(self.url):
            window = WindowCopyTo(self, url=url, to_=to_,  copy=False, new_url=new_url)
            self.parent.wait_window(window)

            if os.path.exists(url.get()):
                self.url = new_url.get()
                logging.info(f'file move to: {new_url.get()}')

    def copy(self):
        logging.info(f'copy ->, {self.url}')
        new_url = tk.StringVar(value='None')
        url = tk.StringVar(value=self.url)
        to_ = tk.StringVar(value=os.path.dirname(self.url))
        if os.path.isfile(self.url):
            option = {'width': 600, 'height': 120}
            window = WindowCopyTo(self, url=url, to_=to_, new_url=new_url, **option)
            self.parent.wait_window(window=window)
            if os.path.exists(new_url.get()):
                logging.info(f"to: {url.get()}")

    def remove(self):
        """Action remove file or delete"""
        from tkinter.messagebox import askyesno
        print('video ->', self.url)
        if os.path.isfile(self.url):
            answer = askyesno(parent=self.parent, title='Confirmation',
                              message='Are you sure that you want to remove?')
            if answer:
                ToolFile.remove(self.url)
                self.destroy()

    def rename(self):
        """Rename the url"""
        logging.info(f"rename -> {self.url}")
        new_url = tk.StringVar(value='None')
        url = tk.StringVar(value=self.url)
        rname = tk.StringVar(value=f"New-{os.path.basename(self.url)}")
        if os.path.isfile(self.url):
            window = OpenDialogRename(self, url=url, rname=rname, new_url=new_url)
            self.parent.wait_window(window)
            # TODO: al cambiar el nombre, modificar self.url base.
            if os.path.exists(url.get()):
                self.url = url.get()
                logging.info(f"renombrado a: {self.url}")
        
    def animate(self):
        # print(counter)
        if not self.animating:
            return
        nt = False
        try:
            nt, frame = self.graphics.get_frame()
        except Exception as e:
            logging.warning(f"exception animate: {str(nt)} {str(e.args)}")
        if nt:
            frame_m = Imagetrans.engine(size=self.size, img=Image.fromarray(frame))
            self.photo = ImageTk.PhotoImage(image=frame_m )
            self.canvas.itemconfig(self.image, image=self.photo)
        self.f_way = round((self.graphics.poss/ 1000), 2)
        
        self.after(self.timer, self.animate)

    def enter(self, event):
        self.animating = True
        self.graphics.set_only_video(self.url)
        self.f_way += self.f_interval
        if self.f_way >= self.graphics.seconds:
            self.f_way = self.f_interval 
        self.graphics.set_poss(self.f_way)
        self.animate()
    
    def leave(self, event):
        self.animating = False
        self.graphics.release()
        self.after_cancel(self.animate)

    def double_click_canvas(self, event):
        #obtener el nombre del fichero de video
        print('video ->', self.url)
        if os.path.isfile(self.url):
            thread = Thread(target=self.tarea, args=("ffplay " + "\"" + self.url + "\"",))
            thread.daemon = True
            thread.start()

    @staticmethod
    def tarea(args=None):
        if not args:
            return
        os.system(args)

    def open(self, file=None):
        if not file: return
        if sys.platform == "win32":
            os.startfile(file)
        else:
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, file])


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("400x800")
    app = SpritePane(root, url='_Work/056af27151ecf1e2ab70fe3afbca6952.mp4', timer=21)
    app.pack()
    SpritePane(root, url='_Work/912350defdcb670ce38c84681c553a33.mp4').pack()
    SpritePane(root, url='_Work/cb696a4ddc356cb2ddad62f57f586bac.mp4').pack()

    root.mainloop()
