import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.constants import X, Y, LEFT, RIGHT, BOTH, YES, TOP
import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, SUCCESS, DANGER
import pyttsx3
import PyPDF2
import pygame
import threading


class AudiobookReader:
    def __init__(self, root):
        self.root = root
        self.root.title("Audiobook Reader")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # Initialize Text-to-Speech Engine
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[0].id)
        self.engine.setProperty("rate", 160)

        # Initialize pygame for playback
        pygame.mixer.init()

        self.text_content = ""
        self.playing = False
        self.paused = False

        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = ttk.Label(
            self.root,
            text="📖 Audiobook Reader",
            font=("Segoe UI", 20, "bold"),
            bootstyle=PRIMARY
        )
        title_label.pack(pady=10)

        # Text box
        self.text_box = tk.Text(
            self.root, wrap="word", font=("Segoe UI", 12), height=15, width=70
        )
        self.text_box.pack(padx=10, pady=10, fill=BOTH, expand=YES)

        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15)

        load_btn = ttk.Button(button_frame, text="Load File", bootstyle=PRIMARY, command=self.load_file)
        load_btn.pack(side=LEFT, padx=5)

        play_btn = ttk.Button(button_frame, text="▶ Play", bootstyle=SUCCESS, command=self.play_text)
        play_btn.pack(side=LEFT, padx=5)

        pause_btn = ttk.Button(button_frame, text="⏸ Pause", bootstyle=PRIMARY, command=self.pause_resume)
        pause_btn.pack(side=LEFT, padx=5)

        stop_btn = ttk.Button(button_frame, text="⏹ Stop", bootstyle=DANGER, command=self.stop_audio)
        stop_btn.pack(side=LEFT, padx=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf"), ("Text Files", "*.txt")]
        )
        if not file_path:
            return

        self.text_content = ""

        try:
            if file_path.endswith(".pdf"):
                with open(file_path, "rb") as pdf_file:
                    reader = PyPDF2.PdfReader(pdf_file)
                    for page in reader.pages:
                        self.text_content += page.extract_text() + "\n"
            else:
                with open(file_path, "r", encoding="utf-8") as txt_file:
                    self.text_content = txt_file.read()

            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, self.text_content)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load file: {str(e)}")

    def play_text(self):
        if not self.text_content.strip():
            messagebox.showwarning("No Text", "Please load a file first.")
            return

        if self.playing:
            self.stop_audio()

        def run_tts():
            self.playing = True
            self.engine.save_to_file(self.text_content, "output.mp3")
            self.engine.runAndWait()
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()

        threading.Thread(target=run_tts, daemon=True).start()

    def pause_resume(self):
        if not self.playing:
            return

        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
        else:
            pygame.mixer.music.unpause()
            self.paused = False

    def stop_audio(self):
        if self.playing:
            pygame.mixer.music.stop()
            self.playing = False
            self.paused = False


if __name__ == "__main__":
    root = ttk.Window(themename="cyborg")  # modern theme
    app = AudiobookReader(root)
    root.mainloop()
