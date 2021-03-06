#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
from axes.photos import Photos
import tkinter as tk
import os, sys, time
import threading
try:
    from .spritepane import SpritePane
    from .photos import Photos
except ImportError:
    from spritepane import SpritePane
    from photos import Photos
from tkinter import filedialog, messagebox
import configparser
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import psutil
import logging

__author__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'GUI tk - ToolTip widget'
__version__ = '1'

__all__ = ('Flowlayout')

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('flowlayou')

extvd = ('.mp4', '.flv', '.avi', '.mpg', '.mkv', 
         '.webm', '.ts', '.mov', '.MP4', '.FLV',
         '.MPG', '.AVI', '.MKV', '.WEBM', '.MOV',
         '.TS')
        
extim = ('.jpeg', '.jpg', '.png', '.gif')


class Flowlayout(tk.Frame):
    def __init__(self, parent=None, *args, **Kvargs):
        super().__init__(parent, *args, **Kvargs)
        self.parent = parent
        self.parent.minsize(400, 400)
        self.split_width, self.split_height = 300, 210
        self.parent.title('gifview')
        # self.parent.iconbitmap('@./../ico/super.ico')
        self.parent['bg'] = 'Yellow'
        self.pack(fill=tk.BOTH, expand=1)
        self.parent.protocol('WM_DELETE_WINDOW', self.confirmExit)
        dirpath = os.path.abspath(os.path.split(os.path.abspath(__file__))[0])
        log.info(dirpath)
        self.dirpathmovies = tk.StringVar(value=dirpath)
        self.setingfile = 'seting.ini'
        self.get_init_status()

        self.textwidget = tk.Text(self, bg='Black')
        self.yscrollbar = tk.Scrollbar(self.textwidget, orient='vertical', command=self.textwidget.yview)
        self.textwidget.configure(yscrollcommand=self.yscrollbar.set)

        self.label = tk.LabelFrame(self)
        self.status_v = tk.StringVar(value=self.dirpathmovies.get())
        self.label_status = tk.Label(self.label, text='label status ...', textvar=self.status_v, bd=1, anchor='w', relief='sunken')
        self.label_status.pack(side=tk.LEFT, fill=tk.X)
        self.boton_s = tk.Button(self.label, text='...', command=self.search_directory)
        self.boton_s.pack(side=tk.RIGHT)

        self.label.pack(side=tk.BOTTOM, fill=tk.X)
        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.textwidget.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.bind_all("<MouseWheel>", self.mouse_scroll)
        self.bind_all("<Button-4>", self.mouse_scroll)
        self.bind_all("<Button-5>", self.mouse_scroll)
        self.parent.bind('<KeyPress>', self.keypress)
        self.thread_load_files()
        self.sprite_list = []

    def about_app(self):
        t = tk.Toplevel(self.parent)
        t.title("AXE APP")
        t.geometry('300x400+100+120')
        t.focus_set()
        t.grab_set()
        t.transient(master=self.parent)
        text = """
        AXE VIEW APP

author  : Hernani Aleman Ferraz
email   : afhernani@gmail.com
apply   : GUI tk - ToolTip widget
version : 2.0

"""
        lbl = tk.Label(t, text=text)
        lbl.pack(padx=10, pady=10)
        ph_ico = Photos()
        lbimg = tk.Label(t, image=ph_ico._spider_scary)
        lbimg.pack(padx=10, pady=10)
        btn = tk.Button(t, text="Aceptar", bg='green', command=t.destroy)
        btn.pack(side=tk.BOTTOM, padx=10, pady=10)
        t.wait_window(t)

    def keypress(self, event):
        if event.keysym == 'i':
            logging.info(f'information: --->')
            self.about_app()
        elif event.keysym == 'x':
            logging.info(f'x: --->')
    
    def get_init_status(self):
        '''
        extract init status of app
        Return:
        '''
        if not os.path.exists(self.setingfile):
            return
        config = configparser.RawConfigParser()
        config.read(self.setingfile)
        try:
            dirpathmovies = config.get('Setings', 'dirpathmovies')
            size = config.get('Setings', 'split_size')
            size = size.split(',')
            self.split_width, self.split_height = int(size[0]), int(size[1])
            geometria = config.get('Setings', 'geometry')
            if geometria:
                self.parent.geometry(geometria)
            if os.path.exists(dirpathmovies):
                self.dirpathmovies.set(dirpathmovies)
                # inicializa la lista con directorio duardao
        except configparser.NoOptionError as e:
            log.warning(str(e.args))

    def set_init_status(self):
        '''
        write init status of app
        Return:
        '''
        config = configparser.RawConfigParser()
        config.add_section('Setings')
        config.set('Setings', 'dirpathmovies', self.dirpathmovies.get())
        config.set('Setings', 'split_size', "%s, %s"%(str(self.split_width), str(self.split_height)))
        config.set('Setings', 'geometry', self.parent.geometry())
        with open(self.setingfile, 'w') as configfile:
            config.write(configfile)
        log.info('Write config file')


    def load_from_file(self):
        if os.path.exists(self.dirpathmovies.get()):
            lista = os.listdir(self.dirpathmovies.get())
            lista.sort()
            for fe in lista:
                if fe.endswith(extvd):
                    fex = os.path.abspath(os.path.join(self.dirpathmovies.get(), fe))
                    log.info(fex)
                    self.textwidget.window_create(tk.INSERT, window=self.load_sprite(arg=fex))
                    time.sleep(0.05) # give some time to load
    
    @staticmethod
    def restart_program():
        """Restarts the current program, with file objects and descriptors cleanup"""
        try:
            p = psutil.Process(os.getpid())
            log.warning(f"id: {os.getpid()}")
            for handler in p.open_files() + p.connections():
                os.close(handler.fd)
        except Exception as e:
            log.error(f"restart Exception: {e}")
        # obtenemos el proceso ejecutable, // psutil.Process(os.getpid()).exe()
        python = sys.executable
        log.warning(f"executable: {python}")
        os.execl(python, python, *sys.argv)
    
    def thread_load_files(self):
        log.info("thread_load_files")
        index = self.textwidget.index(tk.INSERT)
        if index == '1.0':
            log.warning('no tiene contenido')
        else:
            self.set_init_status()
            self.restart_program()
            # self.textwidget.config(state=tk.NORMAL)
            self.textwidget.delete(1.0, tk.END)
            # self.textwidget.delete(tk.INSERT)
            # self.textwidget.config(state=tk.DISABLED)
            for item in self.sprite_list:
                if item:
                    item.destroy()
                    log.info(f"destroyed: {type(item)}")
                else:
                    log.info(f"item destroyed")
            log.info('contenido borrados')
        log.info(f'index -> {index}')
        self.sprite_list = []
        thread = threading.Thread(target=self.load_from_file)
        thread.daemon = True
        thread.start()

    def load_sprite(self, arg):
        if not os.path.isfile(arg):
            log.warning("is not a file")
        # add number of spirtepana to title
        index = self.textwidget.index(tk.INSERT)
        idx = int(str(index).split('.')[1]) + 1
        self.parent.title('gifview :: ' + str(idx))
        options={'width': self.split_width, 'height': self.split_height}
        spt = SpritePane(self.textwidget, url=arg, **options)
        self.sprite_list.append(spt)
        return spt

    def mouse_scroll(self, event):
        # log.info('mouse_scroll_control')
        if event.delta:
            self.textwidget.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1
            self.textwidget.yview_scroll(move, "units")

    def search_directory(self):
        log.info('search directory instruction')
        self.status_v.set('select directory where are movies files to make gif')
        dirname = filedialog.askdirectory(initialdir=self.dirpathmovies.get(), title="Select directory")
        if not dirname == "":
            dir = os.path.abspath(dirname)
            self.dirpathmovies.set(dir)
            self.status_v.set(dir)
            self.thread_load_files()

    def confirmExit(self):
        if messagebox.askokcancel('Quit', 'Are you sure you want to exit?'):
            self.set_init_status()
            self.parent.quit()
        log.info('end process')

def main():
    root = tk.Tk()
    root.geometry("945x650+100+100")
    root.iconphoto(True, tk.PhotoImage(file='appel.png'))
    app = Flowlayout(parent=root)
    app.mainloop()


if __name__ == '__main__':
    main()
