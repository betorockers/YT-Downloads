import os
import tkinter
import tkinter as tk
import customtkinter
import customtkinter as ctk
from PIL import Image, ImageTk
from pytube import YouTube


# Definimos la carpeta de descarga
download_folder = "VideoDownload"

# Creamo la carpeta de descarga si no existe
if not os.path.exists(download_folder):
    os.makedirs(download_folder)


# creamos las funciones necesarias 
# def startDownload(download="D:/proyectos/YT-Downloads/downloaders"):
def startDownload():
    try:
        ytLink = link.get()
        ytObject =YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()
        
        title.configure(text=ytObject.title, text_color="white")
        finishLabel.configure(text="")        
        video.download(output_path=download_folder)
        finishLabel.configure(text="Descarga completada!")
        
    except:
        finishLabel.configure(text="Error de descarga!", text_color="red")


    
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloader = total_size - bytes_remaining    
    #Porcentaje de descarga
    percentage_of_completion = bytes_downloader / total_size * 100
    per = str(int(percentage_of_completion))
    pPercentage.configure(text=per + '%')
    pPercentage.update()
    
    # actualizar barra de progreso
    ProgressBar.set(float(percentage_of_completion) / 100)
    
    



# Configuración del sistema
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")


# configuracion base de la aplicación
app = customtkinter.CTk()
app.iconbitmap("img/2full.ico")
app.geometry("720x480")
app.title("YT VideoDownloader By BetoGraf_inc.")


# Agregamos Elementos ui 
title = customtkinter.CTkLabel(app, text="Edited By @betograf_inc.")
title.pack(padx=10, pady=10)

# agregamos y posicionamos nuestro logo 
logo = customtkinter.CTkImage(light_image=Image.open('img/3.png'), dark_image=Image.open('img/4.png'), size=(200,50))

Label_image = customtkinter.CTkLabel(app, text="", image=logo)
Label_image.pack(padx=15, pady=15)


title = customtkinter.CTkLabel(app, text="Inserta el link de YOUTUBE")
title.pack(padx=20, pady=20)

# Entrada de enlace 
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

#Finish downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Barra de progreso
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

# tamaño de la barra
ProgressBar = customtkinter.CTkProgressBar(app, width=400)
ProgressBar.set(0)
ProgressBar.pack(padx=10, pady=10)



# Downloaad Button
download = customtkinter.CTkButton(app, text="Descargar", command=startDownload)
download.pack(padx=10, pady=10)

#Crear una función para refrescar el campo de entrada
def refrescar_entrada():
    link.delete(0, tk.END)  # Limpiar el campo de entrada

# Crear el botón de refresco
refresh_button = customtkinter.CTkButton(app, text="Refrescar", command=refrescar_entrada)
refresh_button.place(relx=0, y=50, anchor="ne")
refresh_button.pack()

# Run App
app.mainloop()