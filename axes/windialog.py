#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
# import sys
import shutil
from os.path import join
# from functools import partial
import tkinter as tk
from tkinter import Frame, ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showinfo
import threading
import logging

__author__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'GUI tk - Custom File widgets'
__version__ = '1.1.5'

__all__ = ('LabelEntryButton', 'FrameButtons',
           'WindowCopyTo', 'CustomEntry',
           'OpenDialogRename', 'ToolFile')


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('windialog')

class ToolFile(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    @staticmethod
    def copy(origen, destino, *args):
        try:
            shutil.copy(origen, destino)
        except IOError as e:
            showerror(title="Error al copiar",
                      message='Don`t panic!. ' +
                              str(e.args) +
                              origen
                      )

    @staticmethod
    def move(origen, destino, *args):
        try:
            shutil.move(origen, destino)
        except IOError as e:
            showerror(title="Error to move",
                      message='Don`t panic!. ' +
                              str(e.args) +
                              origen
                      )

    @staticmethod
    def remove(origen, *args):
        try:
            os.remove(origen)
        except IOError as e:
            showerror(title="Error to remove",
                      message='Don`t panic!. ' +
                              str(e.args) +
                              origen
                      )


class CustomEntry(tk.Frame):

    text_label: tk.StringVar
    text_entry: tk.StringVar
    label: tk.Label
    entry: tk.Entry

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.text_label = tk.StringVar(value="Label")
        self.text_entry = tk.StringVar(value="Entry")

        self.label = tk.Label(self, text=self.text_label.get())
        self.entry = tk.Entry(self, textvariable=self.text_entry)
        self.entry.focus_set()

        self.label.pack(side=tk.LEFT)  # , expand=True, fill=tk.BOTH)
        self.entry.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


class LabelEntryButton(tk.Frame):

    text_label: tk.StringVar  # = tk.StringVar(value="Label")
    text_entry: tk.StringVar  # = tk.StringVar(value="LabelEntry")
    text_button: tk.StringVar  # = tk.StringVar(value="LabelBoton")

    label: tk.Label
    entry: tk.Entry
    button: tk.Button

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.text_label = tk.StringVar(value='Origen')
        self.text_entry = tk.StringVar(value='')
        self.text_button = tk.StringVar(value='>>')

        self.label = tk.Label(self, text=self.text_label.get())
        self.entry = tk.Entry(self, textvariable=self.text_entry)
        self.entry.focus_set()
        self.button = tk.Button(self, text=self.text_button.get())
        
        self.label.pack(side=tk.LEFT) #, expand=True, fill=tk.BOTH)
        self.entry.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.button.pack(side=tk.RIGHT)


class FrameButtons(tk.Frame):

    btncancelar:tk.Button
    btnaceptar: tk.Button

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.btnaceptar = tk.Button(self, text='Aceptar')
        self.btncancelar = tk.Button(self, text='Cancelar')
        self.btnaceptar.pack(side=tk.RIGHT)
        self.btncancelar.pack(side=tk.RIGHT)


class OpenDialogRename(tk.Toplevel):
    """OpenDialogRename: 
        url = dir to file, rname = new name is known, new_url = dir to file rename
    """
    def __init__(self, parent, url=None, rname=None, new_url=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.geometry('600x120')
        # self.iconbitmap('collage.ico') # pathdir
        self.title('RENAME ...')
        self.wm_protocol("WM_DELETE_WINDOW", self.handlefocus)

        self.focus_force()
        self.transient(master=parent)
        self.grab_set()

        self.new_url = tk.StringVar(value='None') if new_url is  None else new_url

        padding = {'width': 400, 'height': 21, 'padx': 5, 'pady': 5}
        t = None
        self.file = tk.StringVar(value='file to rename') if url is None else url
        name_value = "New_" + os.path.basename(self.file.get())
        self.name = tk.StringVar(value=name_value) if rname is None else rname

        self.feb_ori = LabelEntryButton(self, **padding)
        self.feb_ori.label.configure(text="Archive:   ")
        self.feb_ori.entry.configure(textvariable=self.file)
        self.feb_ori.button.configure(text='>>', command=self.select_archivo)  # state=tk.DISABLED,
        self.feb_ori.pack(fill=tk.BOTH)

        self.ctn_nam = CustomEntry(self, **padding)
        self.ctn_nam.label.configure(text="New name:  ")
        self.ctn_nam.entry.configure(textvariable=self.name)
        self.ctn_nam.pack(fill=tk.BOTH)

        self.btns = FrameButtons(self, **padding)
        self.btns.btnaceptar.configure(command=self.aceptar_click)
        self.btns.btncancelar.configure(command=self.cancelar_click)
        self.btns.pack(fill=tk.BOTH)

    def select_archivo(self):
        filetypes = (
            ('video files', '*.mp4'), ('video files', '*.avi'), ('video files', '*.mkv'),
            ('video files', '*.flv'), ('All files', '*.*')
        )
        initialdir = os.path.dirname(self.file.get())
        filename = fd.askopenfilename(
            parent=self,
            title='Open a file',
            initialdir=initialdir,
            filetypes=filetypes)

        if filename:
            self.file.set(filename)
            self.name.set(os.path.basename(filename))

    def aceptar_click(self):

        origen = self.file.get()
        dirname = os.path.dirname(origen)
        ext = os.path.splitext(origen)[1]
        oldname = os.path.basename(origen)
        name = self.name.get()
        if not ext in name:
            name += ext
        destino = join(dirname, name)
        if not os.path.exists(origen):
            self.select_archivo()
            return
        elif name == '':
            self.name.set("get-the-new-name")
            return
        elif name == oldname:
            self.new_url.set(origen)
            self.destroy()
            self.update()
            return
        
        self.withdraw()
        if oldname != name:
            self.t = threading.Thread(target=ToolFile.move,
                                 args=(origen,
                                       destino,
                                       )
                                 )
            showinfo(title="Renombrando ...", message=f"renombrando {origen} a {destino}")
            self.t.start()
            self.t.join()
            self.new_url.set(destino)
        self.destroy()
        self.update()

    def cancelar_click(self):
        self.destroy()
        self.update()
    
    def handlefocus(self):
        # open a dialog
        # showinfo("Notice", "Are you sure to close the window")
        self.destroy()
        self.update()


class WindowCopyTo(tk.Toplevel):
    """ WindowCopyTo, parameter: copy = True, make a copy. copy=False, move file."""

    def __init__(self, parent, url=None, to_=None, copy=None, new_url=None, *args, **kwargs):
        '''copy = True, make a copy False, move file
            new_url = tk.StringVar where file is copied.
            copy = False, => move to donde_esta.
            url = None, url = tk.SringVar(), to_= tk.StringVar() o None
        '''
        super().__init__(parent, *args, **kwargs)
        
        self.geometry('600x120')
        # self.iconbitmap('collage.ico') # pathdir
        self.title('COPY ...')
        self.wm_protocol("WM_DELETE_WINDOW", self.handlefocus)

        self.focus_force()
        self.transient(master=parent)
        self.grab_set()
        # self.protocol("WM_DELETE_WINDOW", self.destroy)

        t = None # threading
        self.copy = True if copy is None else copy
        if self.copy is False: self.title('MOVE ...')
        self.donde_fue = tk.StringVar() if new_url is  None else new_url

        padding = {'width': 400, 'height': 21, 'padx': 5, 'pady': 5}
        self.file = tk.StringVar(value='archivo') if url is None else url
        self.path_to_copy = tk.StringVar(value='Directorio') if to_ is None else to_

        # Datos origen
        self.feb = LabelEntryButton(self, **padding)
        self.feb.label.configure(text="Origen:    ")
        self.feb.entry.configure(textvariable=self.file)
        self.feb.button.configure(text='>>', command=self.select_archivo) # state=tk.DISABLED,
        self.feb.pack(fill=tk.BOTH)

        # self.feb.entry.insert(0, self.file) o delete(0, 'end')
        # Datos Destino

        self.feb1 = LabelEntryButton(self, **padding)
        self.feb1.label.configure(text="Destino:   ")
        self.feb1.entry.configure(textvariable=self.path_to_copy)
        self.feb1.button.configure(text='. . .', command=self.select_directorio)
        self.feb1.pack(fill=tk.BOTH)

        self.btns = FrameButtons(self, **padding)
        self.btns.btnaceptar.configure(command=self.aceptar_click)
        self.btns.btncancelar.configure(command=self.cancelar_click)
        self.btns.pack(fill=tk.BOTH)

    def handlefocus(self):
        # open a dialog
        # showinfo("Notice", "Are you sure to close the window")
        self.destroy()
        self.update()

    def select_archivo(self):
        filetypes = (
            ('video files', '*.mp4'), ('video files', '*.avi'), ('video files', '*.mkv'),
            ('video files', '*.flv'), ('All files', '*.*')
        )
        initialdir = os.path.dirname(self.file.get())
        filename = fd.askopenfilename(
            parent=self,
            title='Open a file',
            initialdir=initialdir,
            filetypes=filetypes)
        if filename:
            showinfo(title='Selected File',
                    message=filename
                    )
            self.file.set(filename)

    def select_directorio(self):
        initialdir = os.path.dirname(self.file.get())
        directory = fd.askdirectory(parent=self, initialdir=initialdir)
        # showinfo(master=self, title='select_directorio',
        #       message="a lanzado la funcion select_directorio")
        if directory:
            self.path_to_copy.set(directory)

    def aceptar_click(self):

        origen = os.path.abspath(self.file.get())
        name = os.path.basename(self.file.get())
        destino = self.path_to_copy.get()
        if not os.path.exists(origen):
            self.select_archivo()
            return
        elif not os.path.exists(destino):
            self.select_directorio()
            return
        self.withdraw()
        if self.copy:
            self.t = threading.Thread(target=ToolFile.copy,
                                 args=(origen,
                                       destino,
                                       )
                                 )
            showinfo(title="copiando ...", message=f"copiando {name} a {destino}")
        else:
            self.t = threading.Thread(target=ToolFile.move,
                                 args=(origen,
                                       destino,
                                       )
                                 )
            showinfo(title="moviendo ...", message=f"moviendo {name} a {destino}")
        self.t.start()
        self.t.join()
        self.donde_fue.set(os.path.join(destino, name))
        self.destroy()
        self.update()

    def cancelar_click(self):
        self.destroy()
        self.update()


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry('300x120')
        # self.iconbitmap('collage.ico') # pathdir
        self.title('Main Window')


        # place a button on the root window
        ttk.Button(self,
                text='Window copy to ...',
                command=self.win_cp).pack(expand=True)

        ttk.Button(self,
                   text='Window move to ...',
                   command=self.win_mv).pack(expand=True)

        ttk.Button(self,
                   text='Window rename file ...',
                   command=self.win_rn).pack(expand=True)

        ttk.Button(self,
                   text='Delete file ...',
                   command=self.delete).pack(expand=True)

    def win_rn(self):
        """Action rename"""
        local = '/home/hernani/Vídeos/memoriaSwap/Ubuntu-particion-Swap.webp'
        new_url = tk.StringVar(value='None')
        url = tk.StringVar(value=local)
        rname = tk.StringVar(value=f"New_{os.path.basename(local)}")
        window = OpenDialogRename(self, url=url, rname=rname, new_url=new_url)
        self.wait_window(window)
        if os.path.exists(new_url.get()):
            log.info(f"archivo renombrado: {new_url.get()}")
            log.info(f"nuevo nombre: {rname.get()}")

    def win_cp(self):
        """Action copy file"""
        # self.attributes('-disabled', 1)
        local = '/home/hernani/Vídeos/memoriaSwap/Ubuntu-particion-Swap.webp'
        new_url = tk.StringVar(value='Nada')
        url =tk.StringVar(value=local)
        org = tk.StringVar(value=os.path.dirname(local))
        option = {'width': 600, 'height': 120}
        window = WindowCopyTo(self, url=url, to_=org, new_url=new_url, **option)
        
        self.wait_window(window) # .grab_set())
        
        log.info('pass window process')
        log.info(new_url.get())

    def win_mv(self):
        """Action move file"""
        local = '/home/hernani/Vídeos/memoriaSwap/Ubuntu-particion-Swap.webp'
        new_url = tk.StringVar(value='None')
        url =tk.StringVar(value=local)
        org = tk.StringVar(value=os.path.dirname(local))
        window = WindowCopyTo(self,url=url, to_=org, copy=False, new_url=new_url)
        
        # window.grab_set()
        self.wait_window(window)
        if os.path.exists(new_url.get()):
            log.info(new_url.get())

    def delete(self):
        """action delete or remove file"""
        from tkinter.messagebox import askyesno
        url = '/home/hernani/Vídeos/memoriaSwap/Ubuntu-particion-Swap.webp'
        if os.path.isfile(os.path.abspath(url)):
            answer = askyesno(parent=self, title='Confirmation',
                              message='Are you sure that you want to remove?')
            if answer:
                ToolFile.remove(os.path.abspath(url))


if __name__ == "__main__":
    app = App()
    app.mainloop()
