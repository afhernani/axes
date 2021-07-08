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

__author__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'GUI tk - Custom File widgets'
__version__ = '1.1.0'

__all__ = ('LabelEntryButton', 'FrameButtons',
           'WindowCopyTo', 'CustomEntry',
           'OpenDialogRename', 'ToolFile')


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

    file: tk.StringVar
    name: tk.StringVar
    t: threading

    def __init__(self, parent, url=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.geometry('600x120')
        # self.iconbitmap('collage.ico') # pathdir
        self.title('RENAME ...')

        self.url = tk.StringVar() if url is  None else url

        padding = {'width': 400, 'height': 21, 'padx': 5, 'pady': 5}
        self.file = tk.StringVar(value='file')
        self.name = tk.StringVar(value='name')

        self.feb_ori = LabelEntryButton(self, **padding)
        self.feb_ori.label.configure(text="Origen:   ")
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
            ('text files', '*.mp4'),
            ('All files', '*.*')
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir=self.file.get(),
            filetypes=filetypes)

        showinfo(title='Selected File',
                 message=filename
                 )
        self.file.set(filename)

    def aceptar_click(self):

        self.withdraw()

        origen = self.file.get()
        dirname = os.path.dirname(origen)
        ext = os.path.splitext(origen)[1]
        oldname = os.path.basename(origen)
        name = self.name.get()
        if not ext in name:
            name += ext
        destino = join(dirname, name)

        if oldname != name:
            self.t = threading.Thread(target=ToolFile.move,
                                 args=(origen,
                                       destino,
                                       )
                                 )
        showinfo(title="Renombrando ...", message=f"renombrando {origen} a {destino}")
        self.t.start()
        self.url.set(destino)
        self.destroy()
        self.update()

    def cancelar_click(self):
        self.destroy()
        self.update()


class WindowCopyTo(tk.Toplevel):

    file: tk.StringVar
    path_to_copy: tk.StringVar
    t: threading
    copy: bool

    def __init__(self, parent, copy=None, donde_fue=None, *args, **kwargs):
        '''copy = True, make a copy False, move file
            donde_esta = tk.StringVar where file is copied.
            copy = False, => move to donde_esta.
        '''
        super().__init__(parent, *args, **kwargs)
        
        self.geometry('600x120')
        # self.iconbitmap('collage.ico') # pathdir
        self.title('COPY ...')
        self.wm_protocol("WM_DELETE_WINDOW", self.handlefocus)

        self.copy = True if copy is None else copy
        self.donde_fue = tk.StringVar() if donde_fue is  None else donde_fue

        padding = {'width': 400, 'height': 21, 'padx': 5, 'pady': 5}
        self.file = tk.StringVar(value='file')
        self.path_to_copy = tk.StringVar(value='Directorio')

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
            ('text files', '*.mp4'),
            ('All files', '*.*')
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir=self.file.get(),
            filetypes=filetypes)

        showinfo(title='Selected File',
                 message=filename
                 )
        self.file.set(filename)

    def select_directorio(self):
        directory = fd.askdirectory()
        # showinfo(master=self, title='select_directorio',
        #       message="a lanzado la funcion select_directorio")
        self.path_to_copy.set(directory)

    def aceptar_click(self):

        self.withdraw()

        origen = os.path.abspath(self.file.get())
        name = os.path.basename(self.file.get())
        destino = self.path_to_copy.get()

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

    def win_rn(self):
        """Action rename"""
        window = OpenDialogRename(self)
        window.file.set("E:\\Imagenes\\coronavirus.jfif")
        window.name.set("Nevo nombre")
        window.grab_set()

    def win_cp(self):
        """Action copy file"""
        donde_fue = tk.StringVar(value='mi copia')
        option = {'width': 600, 'height': 120}
        window = WindowCopyTo(self, donde_fue=donde_fue, **option)
        # window.title('MOVER ...')
        # window.copy = False
        window.file.set("E:\\Imagenes\\coronavirus.jfif")
        window.path_to_copy.set("E:\\")
        window.wait_window(window.grab_set())
        print(donde_fue.get())

    def win_mv(self):
        """Action move file"""
        url = tk.StringVar()
        window = WindowCopyTo(self, copy=False, donde_fue=url)
        window.title('MOVER ...')
        window.file.set("E:\\Imagenes\\coronavirus.jfif")
        window.path_to_copy.set("E:\\")
        # window.grab_set()
        self.wait_window(window.grab_set())
        if os.path.exists(url.get()):
            print(url.get())

    def delete(self):
        """action delete or remove file"""
        from tkinter.messagebox import askyesno
        url = "E:\\Imagenes\\coronavirus.jfif"
        if os.path.isfile(os.path.abspath(url)):
            answer = askyesno(title='Confirmation',
                              message='Are you sure that you want to remove?')
            if answer:
                ToolFile.remove(os.path.abspath(url))


if __name__ == "__main__":
    app = App()
    app.mainloop()
