import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import tempfile
import pygame
import shutil
from generate import generate_audio, save_audio

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Speech")
        self.audio_file = None
        self.is_playing = False
        self.voice_options = [
            'am_adam', 'am_echo', 'am_eric', 'am_liam', 'am_michael', 
            'am_onyx', 'am_puck', 'af_sky', 'af_heart', 'af_alloy',
            'af_aoede', 'af_bella', 'af_jessica', 'af_kore', 'af_nova',
            'af_river', 'af_sarah', 'bf_alice', 'bf_emma', 'bf_isabella', 
            'bf_lily', 'bm_george', 'bm_lewis', 'bm_daniel', 'bm_fable'
        ]
        self.text_box = scrolledtext.ScrolledText(root, width=60, height=15)
        self.voice_var = tk.StringVar(value='am_michael')
        self.speed_var = tk.DoubleVar(value=1.0)
        control_frame = ttk.Frame(root)
        control_frame.pack(padx=10, pady=5, fill=tk.X)
        ttk.Label(control_frame, text="Voice:").pack(side=tk.LEFT)
        self.voice_menu = ttk.Combobox(control_frame, textvariable=self.voice_var, values=self.voice_options, width=15, state="readonly")
        self.voice_menu.pack(side=tk.LEFT, padx=5)
        ttk.Label(control_frame, text="Speed:").pack(side=tk.LEFT, padx=(10,0))
        self.speed_slider = ttk.Scale(control_frame, from_=0.9, to=1.2, variable=self.speed_var, command=lambda _: self.speed_var.set(round(self.speed_var.get(), 2)))
        self.speed_slider.pack(side=tk.LEFT, padx=5, ipadx=50)
        self.speed_label = ttk.Label(control_frame, textvariable=self.speed_var)
        self.speed_label.pack(side=tk.LEFT)
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=5)
        self.generate_button = ttk.Button(button_frame, text="Generate", command=self.generate_audio)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        self.play_button = ttk.Button(button_frame, text="Play", command=self.toggle_play_pause, state=tk.DISABLED)
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.save_button = ttk.Button(button_frame, text="Save", command=self.save_file, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.text_box.pack(padx=10, pady=10)
        self.text_box.bind("<Control-a>", self.select_all)

    def select_all(self, event):
        event.widget.tag_add("sel", "1.0", "end")
        return "break"

    def generate_audio(self):
        text = self.text_box.get("1.0", tk.END).strip()
        if not text:
            return
        self.audio_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        combined_audio = generate_audio(text, speaker_voice=self.voice_var.get(), voice_speed=round(self.speed_var.get(), 2))
        save_audio(combined_audio, self.audio_file.name)
        self.play_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)

    def toggle_play_pause(self):
        if not self.is_playing:
            pygame.mixer.init()
            pygame.mixer.music.load(self.audio_file.name)
            pygame.mixer.music.play()
            self.is_playing = True
            self.play_button.config(text="Pause")
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.play_button.config(text="Resume")
            else:
                pygame.mixer.music.unpause()
                self.play_button.config(text="Pause")

    def save_file(self):
        if self.audio_file:
            file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
            if file_path:
                shutil.copyfile(self.audio_file.name, file_path)

root = tk.Tk()
app = TextToSpeechApp(root)
root.mainloop()
