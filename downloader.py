import os
from pytubefix import YouTube

# Definimos la carpeta de descarga
DOWNLOAD_FOLDER = "VideoDownloads"

# Creamos la carpeta de descarga si no existe
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_video(url, on_progress_callback):
    """
    Descarga un video de YouTube a partir de una URL.

    Args:
        url (str): URL del video de YouTube a descargar.
        on_progress_callback (function): Función de callback para actualizar el progreso.

    Returns:
        dict: Un diccionario con el estado de la descarga, el título y un mensaje de error si ocurre.
    """
    try:
        yt = YouTube(url, on_progress_callback=on_progress_callback)
        video_stream = yt.streams.get_highest_resolution()
        
        # Inicia la descarga
        video_stream.download(output_path=DOWNLOAD_FOLDER)

        return {
            "success": True, 
            "title": yt.title, 
            "message": "Descarga completada!"
        }
    except Exception as e:
        return {
            "success": False, 
            "title": None, 
            "message": f"Error: {e}"
        }