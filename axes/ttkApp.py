import tkinter as tk
from tkinter import ttk
from ttkasksaveasfile import asksaveasfile_ttk

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejemplo de diálogo modal ttk")
        self.geometry("500x300")
        
        ttk.Label(self, text="Aplicación principal", font=("Segoe UI", 14)).pack(pady=20)
        ttk.Button(self, text="Guardar archivo...", command=self._guardar).pack(pady=10)
        self.label_resultado = ttk.Label(self, text="")
        self.label_resultado.pack(pady=10)
        
    def _guardar(self):
        # Abrimos el diálogo modal
        ruta = asksaveasfile_ttk(
            self,
            titulo="Guardar reporte",
            extensiones=[
                ("Texto plano", ".txt"),
                ("CSV", ".csv"),
                ("JSON", ".json"),
                ("Todos", ".*")
            ]
        )
        
        if ruta:
            self.label_resultado.config(text=f"Se guardará como: {ruta}", foreground="green")
            # Aquí harías: with open(ruta, "w") as f: ...
        else:
            self.label_resultado.config(text="Operación cancelada.", foreground="red")


if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()