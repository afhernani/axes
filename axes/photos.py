#!/usr/bin/env python3
import tkinter as tk
from PIL import Image
import os, sys

__author__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'loadphotos - gifview'
__version__ = '1.4.x'

__all__ = ('Photos')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # base_path = os.path.abspath(".")
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, relative_path)


class Photos():
    def __init__(self):
        self._hacha = tk.PhotoImage(file=resource_path('Assets\\hacha_icon_64px.png'))
        self._spider_scary = tk.PhotoImage(file=resource_path('Assets\\scary_spider_128px.png'))
        self._infection = tk.PhotoImage(file=resource_path('Assets\\infection_malware_256px.png'))
        self._apply = tk.PhotoImage(file=resource_path('Assets\\pirate.png'))
        self._copy = tk.PhotoImage(file=resource_path('Assets\\copy.png'))
        self._delete = tk.PhotoImage(file=resource_path('Assets\\delete.png'))
        self._move = tk.PhotoImage(file=resource_path('Assets\\move.png'))
        self._property = tk.PhotoImage(file=resource_path('Assets\\property.png'))
        self._rename = tk.PhotoImage(file=resource_path('Assets\\rename.png'))
        self._spider = tk.PhotoImage(file=resource_path('Assets\\spider.png'))
        self._sprite = tk.PhotoImage(file=resource_path('Assets\\th.png'))
        self._logo = Image.open(resource_path('Assets\\th.png'))
        # lista de imagenes loading.gif
        self._frames = [tk.PhotoImage(file=resource_path('Assets\\loading.gif'), 
                                      format = 'gif -index %i' %(i)) for i in 
                                      range(Image.open(resource_path('Assets\\loading.gif')).n_frames)]

if __name__ == '__main__':
    root = tk.Tk()
    p = Photos()
