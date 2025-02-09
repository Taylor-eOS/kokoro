import tkinter as tk
from tkinter import scrolledtext
import tempfile
import pygame
from generate import generate_audio, save_audio

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Speech")
        self.audio_file = None

        self.text_box = scrolledtext.ScrolledText(root, width=60, height=15)
        self.text_box.pack(padx=10, pady=10)

        self.generate_button = tk.Button(root, text="Generate", command=self.generate_audio)
        self.generate_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.play_button = tk.Button(root, text="Play", command=self.play_audio, state=tk.DISABLED)
        self.play_button.pack(side=tk.LEFT, padx=5, pady=5)

    def generate_audio(self):
        text = self.text_box.get("1.0", tk.END).strip()
        if not text:
            return
        
        self.audio_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        combined_audio = generate_audio(text)
        save_audio(combined_audio, self.audio_file.name)
        self.play_button.config(state=tk.NORMAL)

    def play_audio(self):
        if self.audio_file:
            pygame.mixer.init()
            pygame.mixer.music.load(self.audio_file.name)
            pygame.mixer.music.play()

root = tk.Tk()
app = TextToSpeechApp(root)
root.mainloop()
