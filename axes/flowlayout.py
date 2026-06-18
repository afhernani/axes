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
        self.parent['bg'] = 'Yellow'
        self.pack(fill=tk.BOTH, expand=1)
        self.parent.protocol('WM_DELETE_WINDOW', self.confirmExit)
        
        dirpath = os.path.abspath(os.path.split(os.path.abspath(__file__))[0])
        log.info(f"Directorio de trabajo: {dirpath}")
        self.dirpathmovies = tk.StringVar(value=dirpath)
        self.setingfile = 'seting.ini'
        self.get_init_status()

        # --- Canvas + Frame para virtualización ---
        self.canvas = tk.Canvas(self, bg='Black', highlightthickness=0)
        self.inner_frame = tk.Frame(self.canvas, bg='Black')
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')
        
        self.yscrollbar = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.yscrollbar.set)
        
        # --- Barra de estado ---
        self.label = tk.LabelFrame(self)
        self.status_v = tk.StringVar(value=self.dirpathmovies.get())
        self.label_status = tk.Label(self.label, text='label status ...', textvariable=self.status_v, bd=1, anchor='w', relief='sunken')
        self.label_status.pack(side=tk.LEFT, fill=tk.X)
        self.boton_s = tk.Button(self.label, text='...', command=self.search_directory)
        self.boton_s.pack(side=tk.RIGHT)
        
        # ORDEN CRÍTICO DE PACK: primero los bordes, al final el que expande
        self.label.pack(side=tk.BOTTOM, fill=tk.X)
        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # --- Variables de virtualización ---
        self.all_files = [] # lista de rutas de archivos en el directorio.
        self.loaded_widgets = {}  # diccionario {indice_global: SpritePane}
        self.padding_x, self.padding_y = 10, 10  # Espacio entre celdas
        self.num_columns = 1  # Se calculará dinámicamente
        self.row_height = self.split_height + self.padding_y  # Altura de cada fila
        self._update_timer_id = None  # Para debounce de scroll
        self._update_scheduled = False # Para evitar múltiples llamadas a update_visible_items
        self._last_scroll_time = 0 # timestamp del último scroll para debounce
        
        # --- Bindings ---
        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)  # NUEVO: detectar cambio de ancho
        self.canvas.bind_all("<MouseWheel>", self.mouse_scroll)
        self.canvas.bind("<Button-4>", self.mouse_scroll)
        self.canvas.bind("<Button-5>", self.mouse_scroll)
        self.parent.bind('<KeyPress>', self.keypress)

        self.load_files()


    def on_canvas_configure(self, event):
        '''Se dispara cuando el canvas cambia de tamaño (ej: redimensionar ventana)'''
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.after(70, self.recalculate_layout)

    def _destroy_all_widgets(self):
        """Destruye todos los SpritePane cargados"""
        for idx, widget in list(self.loaded_widgets.items()):
            try:
                widget.destroy()
            except:
                pass
        self.loaded_widgets.clear()
        self.all_files.clear()
        # resetear el titulo
        self.parent.title('gifview')
        log.info("Todos los widgets destruidos y lista de archivos vaciada.")


    def on_frame_configure(self, event):
        '''Actualiza el scrollregion cuando el frame interno cambia'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def recalculate_layout(self):
        '''Recalcula columnas y redistribuye - MANTIENE SCROLL TOTAL'''
        canvas_width = self.canvas.winfo_width()
        if canvas_width < 10:
            return
        
        new_num_columns = max(1, canvas_width // (self.split_width + self.padding_x))
        
        if new_num_columns != self.num_columns:
            log.info(f"Recalculando: {self.num_columns} -> {new_num_columns} columnas")
            self.num_columns = new_num_columns
            
            # Destruir todos los widgets (cambió la disposición)
            for idx, widget in list(self.loaded_widgets.items()):
                try:
                    widget.destroy()
                except:
                    pass
            self.loaded_widgets.clear()
            
            # Recalcular altura TOTAL
            total_rows = (len(self.all_files) + self.num_columns - 1) // self.num_columns
            new_height = total_rows * self.row_height
            self.inner_frame.configure(height=new_height, width=canvas_width)
            
            # Scrollregion TOTAL (no dinámico)
            self.canvas.configure(scrollregion=(0, 0, canvas_width, new_height))
            
            # Recargar ventana deslizante
            self.after(50, self.update_visible_items)
    
    def _schedule_update(self):
        """Programa la actualización de los elementos visibles con debounce"""
        if self._update_timer_id is not None:
            self.after_cancel(self._update_timer_id)
        self._update_timer_id = self.after(100, self.update_visible_items)

    def update_visible_items(self, event=None):
        '''Carga los SpritePane visibles - VENTANA DESLIZANTE con buffer'''
        self._update_scheduled = False
        
        if not self.all_files or self.num_columns < 1:
            return

        # 1. Obtener posición actual del scroll
        top_y = self.canvas.canvasy(0)
        view_h = self.canvas.winfo_height()
        bottom_y = top_y + view_h

        # 2. Calcular filas visibles con buffer de 1 fila arriba y abajo
        # Si caben 3 filas visibles, cargamos 5 (3 + 1 arriba + 1 abajo)
        start_row = max(0, int(top_y // self.row_height) - 1)
        total_rows = (len(self.all_files) + self.num_columns - 1) // self.num_columns
        end_row = min(total_rows, int(bottom_y // self.row_height) + 2)  # +1 para buffer

        # 3. Convertir a índices globales
        start_idx = start_row * self.num_columns
        end_idx = min(len(self.all_files), (end_row + 1) * self.num_columns)

        visible_indices = set(range(start_idx, end_idx))
        current_indices = set(self.loaded_widgets.keys())

        # 4. Destruir widgets que salieron de la vista
        to_remove = current_indices - visible_indices
        for idx in sorted(to_remove, reverse=True):
            try:
                widget = self.loaded_widgets.pop(idx)
                widget.destroy()
                log.debug(f"Destruyendo índice {idx} (salió de vista)")
            except Exception as e:
                log.error(f"Error al destruir widget {idx}: {e}")

        # 5. Crear widgets que entraron en la vista
        to_add = visible_indices - current_indices
        for idx in sorted(to_add):
            if idx >= len(self.all_files):
                continue
            filepath = self.all_files[idx]
            row, col = divmod(idx, self.num_columns)
            
            try:
                spt = SpritePane(
                    self.inner_frame,
                    url=filepath,
                    width=self.split_width,
                    height=self.split_height
                )
                spt.grid(row=row, column=col, padx=self.padding_x//2, 
                        pady=self.padding_y//2, sticky='nsew')
                self.loaded_widgets[idx] = spt
                log.debug(f"Cargando índice {idx} en fila={row}, col={col}")
            except Exception as e:
                log.error(f"Error al crear widget {filepath}: {e}")

        # Actualizar título con info de ventana deslizante
        visible_count = len(self.loaded_widgets)
        self.parent.title(f'gifview :: {start_idx}-{min(end_idx-1, len(self.all_files)-1)} '
                        f'de {len(self.all_files)} ({visible_count} activos)')

    def mouse_scroll(self, event):
        '''Scroll con ventana deslizante y debounce'''
        if event.delta:
            units = int(-1 * (event.delta / 120))
        else:
            units = 1 if event.num == 5 else -1
        
        self.canvas.yview_scroll(units, "units")
        
        # Programar actualización con debounce (máximo 1 vez cada 50ms)
        current_time = time.time()
        if not self._update_scheduled and (current_time - self._last_scroll_time) > 0.05:
            self._update_scheduled = True
            self._last_scroll_time = current_time
            self.after(50, self.update_visible_items)
        elif not self._update_scheduled:
            self._update_scheduled = True
            self.after(100, self.update_visible_items)


    def load_files(self):
        log.info("load_files: Escaneando directorio...")
        self.status_v.set("Escaneando archivos...")
        
        # Limpiar los spritepane anteriores de forma segura.
        self._destroy_all_widgets()

        dir_path = self.dirpathmovies.get()
        if os.path.exists(dir_path):
            lista = os.listdir(dir_path)
            lista.sort()
            for fe in lista:
                if fe.lower().endswith(extvd):
                    fex = os.path.abspath(os.path.join(dir_path, fe))
                    self.all_files.append(fex)

        log.info(f"Total archivos: {len(self.all_files)}")
        self.after(0, self.on_scan_complete)

    def on_scan_complete(self):
        """Configuración inicial post-escaneo - CALCULAR SCROLL TOTAL"""
        log.info("on_scan_complete: Configurando layout y scroll total...")
        self.status_v.set(f"Listo: {len(self.all_files)} archivos en memoria")
        
        # Calcular columnas iniciales
        canvas_width = self.canvas.winfo_width()
        self.num_columns = max(1, canvas_width // (self.split_width + self.padding_x))
        
        # Calcular altura TOTAL basada en TODOS los archivos
        total_rows = (len(self.all_files) + self.num_columns - 1) // self.num_columns
        total_height = total_rows * self.row_height
        
        # Configurar frame interno
        self.inner_frame.configure(height=total_height, width=canvas_width)
        
        # IMPORTANTE: Scrollregion FIJO basado en el total de archivos
        self.canvas.configure(scrollregion=(0, 0, canvas_width, total_height))
        
        # Cargar primera ventana deslizante
        self.after(100, self.update_visible_items)


    def get_top_visible_index(self):
        """Reemplaza a self.textwidget.index(tk.INSERT) para saber qué se ve"""
        # Obtiene la coordenada Y superior visible en el canvas
        top_y = self.canvas.canvasy(0)
        # Calcula el índice basado en la altura de cada item
        return max(0, int(top_y // self.item_height))


    def load_sprite(self, arg):
        """Método legacy (ya no se usa pero se mantiene por compatibilidad)"""
        if not os.path.isfile(arg):
            log.warning("is not a file")
        index = len(self.loaded_widgets)
        self.parent.title(f'gifview :: {index + 1}')
        options = {'width': self.split_width, 'height': self.split_height}
        spt = SpritePane(self.inner_frame, url=arg, **options)
        return spt


    def search_directory(self):
        log.info('search directory instruction')
        self.status_v.set('Selecciona directorio...')
        dirname = filedialog.askdirectory(initialdir=self.dirpathmovies.get(), title="Select directory")
        if not dirname=="":
            dir_abs = os.path.abspath(dirname)
            self.dirpathmovies.set(dir_abs)
            self.status_v.set(dir_abs)
            self.load_files()

    def confirmExit(self):
        if messagebox.askokcancel('Quit', 'Are you sure you want to exit?'):
            self.set_init_status()
            self.parent.quit()
        log.info('end process')

    def keypress(self, event):
        if event.keysym == 'i':
            self.about_app()

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
        version : 2.0
        """
        lbl = tk.Label(t, text=text)
        lbl.pack(padx=10, pady=10)
        btn = tk.Button(t, text="Aceptar", bg='green', command=t.destroy)
        btn.pack(side=tk.BOTTOM, padx=10, pady=10)
        t.wait_window(t)

    def get_init_status(self):
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
        except configparser.NoOptionError as e:
            log.warning(str(e.args))

    def set_init_status(self):
        config = configparser.RawConfigParser()
        config.add_section('Setings')
        config.set('Setings', 'dirpathmovies', self.dirpathmovies.get())
        config.set('Setings', 'split_size', "%s, %s" % (str(self.split_width), str(self.split_height)))
        config.set('Setings', 'geometry', self.parent.geometry())
        with open(self.setingfile, 'w') as configfile:
            config.write(configfile)
        log.info('Write config file')

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

def main():
    root = tk.Tk()
    root.geometry("945x650+100+100")
    root.iconphoto(True, tk.PhotoImage(file='appel.png'))
    app = Flowlayout(parent=root)
    app.mainloop()


if __name__ == '__main__':
    main()
