#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
import tkinter as tk
import os
import threading
from spritepane import SpritePane
from tkinter import filedialog, messagebox
import configparser
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
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
         '.MPG', '.AVI', '.MKV', 'WEBM', '.MOV',
         '.TS')
        
extim = ('.jpeg', '.jpg', '.png', '.gif')


class Flowlayout(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
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
        self.thread_load_files()

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
        with open(self.setingfile, 'w') as configfile:
            config.write(configfile)
        log.info('Write config file')


    def load_from_file(self):
        if os.path.exists(self.dirpathmovies.get()):
            for fe in os.listdir(self.dirpathmovies.get()):
                if fe.endswith(extvd):
                    fex = os.path.abspath(os.path.join(self.dirpathmovies.get(), fe))
                    log.info(fex)
                    self.textwidget.window_create(tk.INSERT, window=self.load_sprite(arg=fex))

    def thread_load_files(self):
        index = self.textwidget.index(tk.INSERT)
        if index == '1.0':
            log.warning('no tiene contenido')
        else:
            self.textwidget.config(state=tk.NORMAL)
            self.textwidget.delete(1.0, tk.END)
            self.textwidget.delete(tk.INSERT)
            self.textwidget.config(state=tk.DISABLED)
            log.info('contenido borrados')
        log.info(f'index -> {index}')
        thread = threading.Thread(target=self.load_from_file)
        thread.daemon = True
        thread.start()

    def load_sprite(self, arg):
        if not os.path.isfile(arg):
            log.warning("is not a file")
        # add number of spirtepana to title
        index = self.textwidget.index(tk.INSERT)
        idx = str(index).split('.')[1]
        self.parent.title('gifview :: ' + idx)
        return SpritePane(self.textwidget, url=arg)

    def mouse_scroll(self, event):
        log.info('mouse_scroll_control')
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
