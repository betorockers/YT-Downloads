import customtkinter as ctk
from app import VideoDownloaderApp

if __name__ == "__main__":
    # Configuracion del sistema
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    # Iniciar la aplicación
    app = VideoDownloaderApp()
    app.mainloop()