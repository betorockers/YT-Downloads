import threading
import tkinter as tk
import customtkinter as ctk
from PIL import Image
import re
import os

from downloader import download_video

# --- Clase principal de la aplicación ---
class VideoDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración base de la ventana
        self.geometry("720x480")
        self.title("YT VideoDownloader By BetoGraf_inc.")
        
        # Grid layout para una mejor organización de la UI
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        """Crea y posiciona todos los elementos de la interfaz de usuario."""
        
        # Frame principal para contener todos los elementos
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Añadir logo de la aplicación
        try:
            logo_path_light = "img/logoBlancoGraf.png"
            logo_path_dark = "img/logoNegroGraf.png"
            if os.path.exists(logo_path_light) and os.path.exists(logo_path_dark):
                self.logo = ctk.CTkImage(
                    light_image=Image.open(logo_path_light),
                    dark_image=Image.open(logo_path_dark),
                    size=(290, 80)
                )
                self.logo_label = ctk.CTkLabel(main_frame, text="", image=self.logo)
                self.logo_label.pack(pady=(10, 5))
            else:
                self.logo_label = ctk.CTkLabel(main_frame, text="YT Downloader", font=("Roboto", 24))
                self.logo_label.pack(pady=(10, 5))
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            self.logo_label = ctk.CTkLabel(main_frame, text="YT Downloader", font=("Roboto", 24))
            self.logo_label.pack(pady=(10, 5))
            
        # Título de la aplicación
        self.title_label = ctk.CTkLabel(main_frame, text="Inserta el link de YouTube", font=("Roboto", 18))
        self.title_label.pack(pady=(10, 5))
        
        # Campo de entrada para el enlace
        self.url_var = tk.StringVar()
        self.link_entry = ctk.CTkEntry(main_frame, width=400, height=40, placeholder_text="Pega aquí el enlace del video", textvariable=self.url_var)
        self.link_entry.pack(pady=(0, 10))
        
        # Etiqueta para el título del video (se actualizará dinámicamente)
        self.video_title_label = ctk.CTkLabel(main_frame, text="", font=("Roboto", 14), text_color="cyan")
        self.video_title_label.pack()

        # Etiqueta para el estado de la descarga
        self.status_label = ctk.CTkLabel(main_frame, text="", font=("Roboto", 14))
        self.status_label.pack(pady=(5, 5))
        
        # Barra de progreso
        self.progress_bar = ctk.CTkProgressBar(main_frame, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(5, 10))

        # Etiqueta para el porcentaje de descarga
        self.percentage_label = ctk.CTkLabel(main_frame, text="0%")
        self.percentage_label.pack(pady=(0, 10))
        
        # Botones de acción
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=(10, 10))
        
        self.download_button = ctk.CTkButton(
            button_frame, 
            text="Descargar Video", 
            command=self.start_download_thread
        )
        self.download_button.pack(side="left", padx=10)
        
        self.refresh_button = ctk.CTkButton(
            button_frame, 
            text="Refrescar", 
            command=self.refresh_entry
        )
        self.refresh_button.pack(side="right", padx=10)
    
    # --- Lógica de la aplicación ---
    def start_download_thread(self):
        """Inicia la descarga en un hilo separado para no congelar la UI."""
        url = self.url_var.get()
        
        # Validación de la URL de YouTube
        if not re.match(r"^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$", url):
            self.status_label.configure(text="Enlace no válido. Por favor, revisa la URL.", text_color="red")
            return
        
        self.status_label.configure(text="Conectando...", text_color="yellow")
        self.update()
        
        download_thread = threading.Thread(target=self.run_download, args=(url,))
        download_thread.start()

    def run_download(self, url):
        """Ejecuta la función de descarga y actualiza la UI al finalizar."""
        result = download_video(url, self.on_progress)
        
        if result["success"]:
            self.video_title_label.configure(text=f"Título: {result['title']}")
            self.status_label.configure(text=result['message'], text_color="green")
        else:
            self.status_label.configure(text=result['message'], text_color="red")
            self.video_title_label.configure(text="")
            self.progress_bar.set(0)
            self.percentage_label.configure(text="0%")

    def on_progress(self, stream, chunk, bytes_remaining):
        """Actualiza la barra de progreso y el porcentaje."""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        
        percentage = (bytes_downloaded / total_size) * 100
        
        self.percentage_label.configure(text=f"{int(percentage)}%")
        self.progress_bar.set(percentage / 100)
        self.update()

    def refresh_entry(self):
        """Limpia todos los campos y etiquetas de la UI."""
        self.url_var.set("")
        self.video_title_label.configure(text="")
        self.status_label.configure(text="")
        self.percentage_label.configure(text="0%")
        self.progress_bar.set(0)