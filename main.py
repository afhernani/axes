#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
import tkinter as tk

from axes import Flowlayout

def main():
    root = tk.Tk()
    root.geometry("945x650+100+100")
    root.iconphoto(True, tk.PhotoImage(file='appel.png'))
    app = Flowlayout(parent=root)
    app.mainloop()


if __name__ == '__main__':
    main()