import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import importar  
import ventana_logs

class InterfazPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Loglytics")
        self.root.geometry("400x450")
        self.root.config(bg="#039be5")  # Color azul de fondo de la ventana principal

        # Marco principal
        self.marco = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        self.marco.place(relx=0.5, rely=0.5, anchor="center", width=300, height=400)

        # Logo
        self.cargar_logo()
        
        # Título
        self.titulo = tk.Label(self.marco, text="LOGLYTICS", font=("Arial", 24, "bold"), fg="#6200ea", bg="white")
        self.titulo.pack(pady=(10, 20))

        # Botón de Importar Logs
        self.boton_importar = tk.Button(self.marco, text="📥 Importar Logs", font=("Arial", 12, "bold"), bg="#039be5", fg="black", command=self.importar_logs)
        self.boton_importar.pack(pady=(10, 10), ipadx=10, ipady=5)

        # Botón de Iniciar Análisis
        self.boton_analisis = tk.Button(self.marco, text="🔍 Iniciar análisis", font=("Arial", 12, "bold"), bg="#039be5", fg="black", command=self.iniciar_analisis)
        self.boton_analisis.pack(pady=(10, 10), ipadx=10, ipady=5)

        # Botón de Salir
        self.boton_salir = tk.Button(self.marco, text="Salir", font=("Arial", 12, "bold"), bg="#039be5", fg="black", command=self.root.quit)
        self.boton_salir.pack(pady=(10, 10), ipadx=20, ipady=5)

    def cargar_logo(self):
        # Cargar y ajustar la imagen del logo
        try:
            imagen = Image.open("logo.png")  # Asegúrate de tener "logo.png" en el mismo directorio
            imagen = imagen.resize((100, 100), Image.LANCZOS)  # Reemplaza Image.ANTIALIAS con Image.LANCZOS
            self.logo_img = ImageTk.PhotoImage(imagen)
            self.logo_label = tk.Label(self.marco, image=self.logo_img, bg="white")
            self.logo_label.pack(pady=(10, 0))
        except FileNotFoundError:
            messagebox.showwarning("Advertencia", "No se encontró la imagen del logo")

    def importar_logs(self):
        # Acción del botón Importar Logs
        try:
            # Llamamos a la función del módulo importar solo cuando el usuario presiona el botón
            importar.importar()  # Llama a la función que procesa el archivo
            messagebox.showinfo("Archivo procesado", "El archivo de logs ha sido importado y procesado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al procesar el archivo: {e}")

    def iniciar_analisis(self):
        # Acción del botón Iniciar Análisis
        try:
            # Llamamos a la función del módulo importar solo cuando el usuario presiona el botón
            messagebox.showinfo("Analisis terminado", "El archivo de logs ha sido analizado correctamente.")
            ventana_logs.implementar()  # Llama a la función que procesa el archivo
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al analizar el archivo: {e}")

# Configuración de la ventana principal
root = tk.Tk()
app = InterfazPrincipal(root)
root.mainloop()