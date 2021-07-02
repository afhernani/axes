#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import tkinter as tk
# from tkinter import ttk

__author__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'GUI tk - ToolTipMenu widget'
__version__ = '1'

__all__ = ('ToolTipMenu', 'createToolTipMenu')


class ToolTipMenu(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.menu = None
        self.x = self.y = 0

    def showtipMenu(self, menu, event):
        '''Display Menu in tooltipMenu window'''

        self.menu = menu
        if self.tipwindow or not self.menu:
            return
        menu.tk_popup(event.x_root, event.y_root)


def createToolTipMenu(widget, menu):

    toolTipMenu = ToolTipMenu(widget)

    def popup(event):
        toolTipMenu.showtipMenu(menu, event)

    widget.bind('<Button-3>', popup)

    return toolTipMenu
