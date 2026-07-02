import tkinter as tk
from tkinter import ttk
from pathlib import Path

class DialogoGuardarArchivo(tk.Toplevel):
    """Diálogo modal personalizado para guardar un archivo."""
    
    def __init__(self, parent, titulo="Guardar como", extensiones=None):
        super().__init__(parent)
        self.title(titulo)
        self.resultado = None  # Aquí guardaremos la ruta final
        self.parent = parent
        
        # Configuración de la ventana
        self.geometry("450x220")
        self.resizable(False, False)
        self.transient(parent)      # Vinculada a la ventana padre
        self.grab_set()             # ¡Esto la hace MODAL!
        
        # Variables
        self.nombre_var = tk.StringVar()
        self.extension_var = tk.StringVar()
        extensiones = extensiones or [("Texto", ".txt"), ("CSV", ".csv"), ("JSON", ".json")]
        self.extensiones = extensiones
        self.extension_var.set(extensiones[0][1])
        
        self._construir_ui()
        
        # Hacer que se cierre con ESC y Enter confirme
        self.bind("<Escape>", lambda e: self._cancelar())
        self.bind("<Return>", lambda e: self._aceptar())
        
        # Centrar sobre la ventana padre
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (450 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (220 // 2)
        self.geometry(f"+{x}+{y}")
        
        self.nombre_entry.focus_set()
        
    def _construir_ui(self):
        # Marco principal con padding
        marco = ttk.Frame(self, padding=15)
        marco.pack(fill=tk.BOTH, expand=True)
        
        # Etiqueta + Entry para el nombre
        ttk.Label(marco, text="Nombre del archivo:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.nombre_entry = ttk.Entry(marco, textvariable=self.nombre_var, width=40)
        self.nombre_entry.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 10))
        
        # Combobox para la extensión
        ttk.Label(marco, text="Tipo de archivo:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        valores_combo = [f"{nombre} ({ext})" for nombre, ext in self.extensiones]
        self.combo = ttk.Combobox(marco, values=valores_combo, state="readonly", width=37)
        self.combo.current(0)
        self.combo.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))
        self.combo.bind("<<ComboboxSelected>>", self._cambiar_extension)
        
        # Botones
        marco_botones = ttk.Frame(marco)
        marco_botones.grid(row=4, column=0, columnspan=2, sticky=tk.E)
        
        ttk.Button(marco_botones, text="Cancelar", command=self._cancelar).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(marco_botones, text="Guardar", command=self._aceptar).pack(side=tk.RIGHT)
        
        marco.columnconfigure(0, weight=1)
        
    def _cambiar_extension(self, evento=None):
        idx = self.combo.current()
        self.extension_var.set(self.extensiones[idx][1])
        
    def _aceptar(self):
        nombre = self.nombre_var.get().strip()
        if not nombre:
            # Mostrar aviso si está vacío
            from tkinter import messagebox
            messagebox.showwarning("Atención", "Debes introducir un nombre de archivo.", parent=self)
            return
        
        # Quitar extensión si el usuario la puso, para evitar duplicados
        nombre = Path(nombre).stem
        # Construir la ruta completa
        self.resultado = f"{nombre}{self.extension_var.get()}"
        self.grab_release()
        self.destroy()
        
    def _cancelar(self):
        self.resultado = None
        self.grab_release()
        self.destroy()