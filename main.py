# ! /usr/bin/env python3
# -*- coding:UTF-8 -*-
import tkinter as tk
from axes import Flowlayout
from axes.photos import resource_path

def main():
    root = tk.Tk()
    root.geometry("945x650+100+100")
    root.iconphoto(True, tk.PhotoImage(file=resource_path('assets\\text_log_32x32.png')))
    app = Flowlayout(parent=root)
    app.mainloop()


if __name__ == '__main__':
    main()