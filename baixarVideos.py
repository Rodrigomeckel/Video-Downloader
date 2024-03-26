import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Combobox
from pytube import YouTube
from threading import Thread

def choose_download_path():
    download_path = filedialog.askdirectory()
    if download_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, download_path)

def download_progress(stream, chunk, remaining):
    percent = (100 * (stream.filesize - remaining)) / stream.filesize
    progress_bar["value"] = percent
    root.update_idletasks()

def download_video():
    url = url_entry.get()
    path = path_entry.get()
    quality = quality_combobox.get()

    try:
        yt = YouTube(url, on_progress_callback=download_progress)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', res=quality).first()
        if stream:
            progress_bar["value"] = 0
            download_button.config(state=tk.DISABLED)
            Thread(target=stream.download, args=(path,), daemon=True).start()
        else:
            messagebox.showerror("Erro", "Nenhum stream adequado disponível para download.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        download_button.config(state=tk.NORMAL)

root = tk.Tk()
root.title("Baixar videos do YouTube")
root.geometry("500x300")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

url_label = tk.Label(root, text="Video URL:", bg="#f0f0f0")
url_entry = tk.Entry(root, width=50)
path_label = tk.Label(root, text="Pasta de Download:", bg="#f0f0f0")
path_entry = tk.Entry(root, width=50)
browse_button = tk.Button(root, text="Pesquisar", command=choose_download_path)
quality_label = tk.Label(root, text="Qualidade do video:", bg="#f0f0f0")
quality_combobox = Combobox(root, values=["360p", "720p", "1080p"])  # Add more options as needed
download_button = tk.Button(root, text="Download Video", command=download_video)
progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')

url_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
path_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
path_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
browse_button.grid(row=1, column=2, padx=5, pady=5)
quality_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
quality_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
download_button.grid(row=3, columnspan=3, padx=5, pady=5)
progress_bar.grid(row=4, columnspan=3, padx=5, pady=5)

root.mainloop()