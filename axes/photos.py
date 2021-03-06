#!/usr/bin/env python3
import tkinter as tk
try:
    from PIL import Image
except ImportError:
    print('Error to load PIL lib, try: pip install pillow')
import os, sys

__author__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'loadphotos - gifview'
__version__ = '1.3.x'

__all__ = ('Photos')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Photos():
    def __init__(self):
        self._hacha = tk.PhotoImage(file=resource_path('Images/hacha_icon_64px.png'))
        self._spider_scary = tk.PhotoImage(file=resource_path('Images/scary_spider_128px.png'))
        self._infection = tk.PhotoImage(file=resource_path('Images/infection_malware_256px.png'))
        self._apply = tk.PhotoImage(file=resource_path('Images/pirate.png'))
        self._copy = tk.PhotoImage(file=resource_path('Images/copy.png'))
        self._delete = tk.PhotoImage(file=resource_path('Images/delete.png'))
        self._move = tk.PhotoImage(file=resource_path('Images/move.png'))
        self._property = tk.PhotoImage(file=resource_path('Images/property.png'))
        self._rename = tk.PhotoImage(file=resource_path('Images/rename.png'))
        self._spider = tk.PhotoImage(file=resource_path('Images/spider.png'))
        self._sprite = tk.PhotoImage(file=resource_path('Images/th.png'))
        self._logo = Image.open(resource_path('Images/th.png'))
        # lista de imagenes loading.gif
        self._frames = [tk.PhotoImage(file=resource_path('Images/loading.gif'), format = 'gif -index %i' %(i)) for i in range(Image.open(resource_path('Images/loading.gif')).n_frames)]

if __name__ == '__main__':
    root = tk.Tk()
    p = Photos()
