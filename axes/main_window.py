#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Ventana principal que lanza la aplicación de video como ventana modal.
"""
import tkinter as tk
from tkinter import ttk, Toplevel
from tkinter.messagebox import showinfo
import os
import sys

# Importamos la clase App de modcv
from modcv import App as VideoApp


class MainWindow:
    """Ventana principal con botones para lanzar funcionalidades."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Panel de Control - Aplicaciones")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Centrar la ventana
        self._center_window(400, 300)
        
        # Configurar estilo
        self._setup_styles()
        
        # Crear interfaz
        self._create_widgets()
    
    def _center_window(self, width, height):
        """Centra la ventana en la pantalla."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _setup_styles(self):
        """Configura los estilos de la interfaz."""
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Action.TButton', font=('Arial', 11), padding=10)
    
    def _create_widgets(self):
        """Crea los widgets de la ventana principal."""
        # Título
        title_label = ttk.Label(
            self.root, 
            text="🎬 Panel de Control", 
            style='Title.TLabel'
        )
        title_label.pack(pady=20)
        
        # Descripción
        desc_label = ttk.Label(
            self.root,
            text="Selecciona una aplicación para abrir:",
            font=('Arial', 10)
        )
        desc_label.pack(pady=5)
        
        # Frame para los botones
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=30)
        
        # Botón para abrir el reproductor de video
        self.btn_video = ttk.Button(
            button_frame,
            text="🎥 Abrir Reproductor de Video",
            command=self._open_video_app,
            style='Action.TButton'
        )
        self.btn_video.pack(pady=10, padx=20, fill=tk.X)
        
        # Botón de ejemplo adicional (puedes añadir más)
        self.btn_other = ttk.Button(
            button_frame,
            text="📊 Otra Aplicación (ejemplo)",
            command=self._show_placeholder,
            style='Action.TButton'
        )
        self.btn_other.pack(pady=10, padx=20, fill=tk.X)
        
        # Label de estado
        self.status_label = ttk.Label(
            self.root,
            text="Listo",
            font=('Arial', 9),
            foreground='gray'
        )
        self.status_label.pack(side=tk.BOTTOM, pady=10)
    
    def _open_video_app(self):
        """Abre la aplicación de video como ventana modal."""
        self.status_label.config(text="Abriendo reproductor...")
        
        # Crear ventana secundaria (Toplevel)
        video_window = Toplevel(self.root)
        video_window.title("Reproductor de Video")
        
        # Hacer la ventana modal (bloquea la ventana principal)
        video_window.transient(self.root)  # Sigue a la ventana padre
        video_window.grab_set()  # MODAL: bloquea interacción con padre
        
        # Ruta del video (puedes cambiarla o pedir al usuario)
        video_source = "../_Work/023Nf32.avi"
        
        # Verificar si el archivo existe
        if not os.path.exists(video_source):
            # Si no existe, usar webcam por defecto
            video_source = 0
        
        try:
            # IMPORTANTE: run_mainloop=False porque YA estamos en un mainloop
            self.video_app = VideoApp(
                window=video_window,
                window_title="Reproductor de Video",
                video_source=video_source,
                run_mainloop=False  # CLAVE: no ejecutar otro mainloop
            )
            
            # Cuando se cierre la ventana, liberar recursos
            video_window.protocol("WM_DELETE_WINDOW", self._on_video_window_close)
            
            self.status_label.config(text="Reproductor abierto")
            
        except Exception as e:
            from tkinter.messagebox import showerror
            showerror("Error", f"No se pudo abrir el reproductor:\n{str(e)}")
            video_window.destroy()
            self.status_label.config(text="Error al abrir")
    
    def _on_video_window_close(self):
        """Se ejecuta cuando se cierra la ventana de video."""
        try:
            # Liberar recursos del video
            if hasattr(self, 'video_app') and self.video_app:
                self.video_app.vid.release()
        except Exception as e:
            print(f"Error al liberar recursos: {e}")
        
        # Destruir la ventana
        self.root.grab_release()  # Liberar el modal
        self.root.nametowidget(str(self.video_app.window)).destroy()
        self.status_label.config(text="Reproductor cerrado")
    
    def _show_placeholder(self):
        """Muestra un mensaje placeholder."""
        showinfo("Info", "Esta es una aplicación de ejemplo.\nAquí podrías añadir otra funcionalidad.")


if __name__ == '__main__':
    # Crear la ventana principal
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()