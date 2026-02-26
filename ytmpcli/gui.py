import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
from .downloader import download_media

class YTmpcliGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ytmpcli - YouTube Downloader")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TFrame", padding=10)

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.main_frame, text="YouTube URL:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.url_entry = ttk.Entry(self.main_frame, width=60)
        self.url_entry.pack(fill=tk.X, pady=(0, 15))
        self.url_entry.focus()

        options_frame = ttk.LabelFrame(self.main_frame, text="Download Options", padding=10)
        options_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(options_frame, text="Format:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.format_var = tk.StringVar(value="mp3")
        ttk.Radiobutton(options_frame, text="MP3 (Audio)", variable=self.format_var, value="mp3").grid(row=0, column=1, padx=10)
        ttk.Radiobutton(options_frame, text="MP4 (Video)", variable=self.format_var, value="mp4").grid(row=0, column=2, padx=10)

        ttk.Label(options_frame, text="Type:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=10)
        self.mode_var = tk.StringVar(value="single")
        ttk.Radiobutton(options_frame, text="Single Video", variable=self.mode_var, value="single").grid(row=1, column=1, padx=10)
        ttk.Radiobutton(options_frame, text="Playlist", variable=self.mode_var, value="playlist").grid(row=1, column=2, padx=10)

        self.download_btn = ttk.Button(self.main_frame, text="Download Now", command=self.start_download_thread)
        self.download_btn.pack(pady=10)

        self.status_var = tk.StringVar(value="Ready to download.")
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var, wraplength=450, foreground="blue")
        self.status_label.pack(pady=10)

        self.progress = ttk.Progressbar(self.main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a valid YouTube URL.")
            return

        self.download_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.status_var.set("Working... please wait.")
        
        thread = threading.Thread(target=self.run_download, args=(url,), daemon=True)
        thread.start()

    def run_download(self, url):
        is_playlist = self.mode_var.get() == "playlist"
        file_format = self.format_var.get()
        
        try:
            download_media(url, is_playlist=is_playlist, file_format=file_format)
            self.root.after(0, self.on_success)
        except Exception as e:
            self.root.after(0, lambda: self.on_error(str(e)))

    def on_success(self):
        self.progress.stop()
        self.download_btn.config(state=tk.NORMAL)
        self.status_var.set("Download completed successfully!")
        messagebox.showinfo("Success", "Download finished!")

    def on_error(self, error_msg):
        self.progress.stop()
        self.download_btn.config(state=tk.NORMAL)
        self.status_var.set(f"Error: {error_msg}")
        messagebox.showerror("Download Error", f"An error occurred: {error_msg}")

def main():
    root = tk.Tk()
    app = YTmpcliGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
