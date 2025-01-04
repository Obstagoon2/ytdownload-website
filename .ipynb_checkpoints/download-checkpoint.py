import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp

def download_video():
    url = url_entry.get()
    save_path = filedialog.askdirectory()

    if not url or not save_path:
        messagebox.showerror("Error", "Please provide a valid URL and select a save location.")
        return

    try:
        ydl_opts = {
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'format': 'bestaudio/best' if format_var.get() == 'mp3' else 'best',
        }

        # Add postprocessor only if format is MP3
        if format_var.get() == 'mp3':
            ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Success", "Download completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main application window
app = tk.Tk()
app.title("YouTube to MP3/MP4 Converter")
app.geometry("400x200")

# URL Label and Entry
url_label = tk.Label(app, text="YouTube Video URL:")
url_label.pack(pady=5)

url_entry = tk.Entry(app, width=50)
url_entry.pack(pady=5)

# Format Selection
format_var = tk.StringVar(value="mp4")
mp3_radio = tk.Radiobutton(app, text="MP3", variable=format_var, value="mp3")
mp3_radio.pack(pady=5)

mp4_radio = tk.Radiobutton(app, text="MP4", variable=format_var, value="mp4")
mp4_radio.pack(pady=5)

# Download Button
download_button = tk.Button(app, text="Download", command=download_video)
download_button.pack(pady=20)

# Run the application
app.mainloop()
