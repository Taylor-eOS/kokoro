import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import tempfile
import pygame
import shutil
import pysbd
import re
from generate import generate_audio, save_audio

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Speech")
        self.audio_file = None
        self.is_playing = False
        self.autosplit_var = tk.BooleanVar(value=True)
        self.voice_options = ['af_sky', 'am_michael', 'am_adam', 'am_eric', 'am_liam', 'bm_george', 'bm_lewis', 'bm_daniel', 'af_heart', 'bf_alice', 'am_onyx', 'af_alloy', 'af_bella', 'af_aoede', 'af_jessica', 'af_sarah', 'af_nova', 'af_river', 'bf_isabella', 'bf_lily', 'bf_emma', 'am_echo', 'af_kore', 'am_puck', 'bm_fable']
        self.text_box = scrolledtext.ScrolledText(root, width=60, height=15)
        self.voice_var = tk.StringVar(value='af_sky')
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
        self.generate_button = ttk.Button(button_frame, text="Generate", command=self.generate_app_audio)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        self.play_button = ttk.Button(button_frame, text="Play", command=self.toggle_play_pause, state=tk.DISABLED)
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.save_button = ttk.Button(button_frame, text="Save", command=self.save_file, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.autosplit_check = ttk.Checkbutton(
            button_frame, 
            text="Automatic sentence splitting", 
            variable=self.autosplit_var)
        self.autosplit_check.pack(side=tk.LEFT, padx=10)
        self.text_box.pack(padx=10, pady=10)
        self.hard_area_label = ttk.Label(root, text="Each line gets processed separately. Segment your text accordingly.", foreground="gray")
        self.hard_area_label.pack(padx=10, pady=(0, 10))
        self.text_box.bind("<Control-a>", self.select_all)
        self.is_paused = False

    def split_sentences(self, text):
        PARAGRAPH_PLACEHOLDER = "||PARAGRAPH||"
        paragraph_breaks = re.split(r'(\n{2,})', text)
        segmenter = pysbd.Segmenter(language="en", clean=True)
        elements = []
        for part in paragraph_breaks:
            if not part:
                continue
            if re.match(r'\n{2,}', part):
                elements.append(PARAGRAPH_PLACEHOLDER)
            else:
                elements.extend(segmenter.segment(part.strip()))
        processed = []
        for el in elements:
            if el == PARAGRAPH_PLACEHOLDER:
                processed.append("\n\n")
            else:
                processed.append(el + "\n\n")
        return "".join(processed).strip()

    def generate_app_audio(self):
        text = self.text_box.get("1.0", tk.END).strip()
        if not text:
            return
        if self.autosplit_var.get():
            text = self.split_sentences(text)
        self.audio_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        combined_audio = generate_audio(text, speaker_voice=self.voice_var.get(), voice_speed=round(self.speed_var.get(), 2))
        save_audio(combined_audio, self.audio_file.name)
        self.play_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
        self.is_playing = False
        self.play_button.config(text="Play")
        pygame.mixer.quit()
        self.is_playing = False
        self.play_button.config(text="Play")
        self.is_paused = False

    def toggle_play_pause(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.is_paused = True
            self.play_button.config(text="Resume")
        else:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_playing = True
                self.is_paused = False
                self.play_button.config(text="Pause")
            else:
                pygame.mixer.music.load(self.audio_file.name)
                pygame.mixer.music.play()
                self.is_playing = True
                self.play_button.config(text="Pause")
            self.root.after(100, self.check_playback_status)

    def check_playback_status(self):
        if self.is_paused or pygame.mixer.music.get_busy():
            self.root.after(100, self.check_playback_status)
        else:
            self.is_playing = False
            self.play_button.config(text="Play")

    def save_file(self):
        if self.audio_file:
            file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
            if file_path:
                shutil.copyfile(self.audio_file.name, file_path)

    def select_all(self, event):
        event.widget.tag_add("sel", "1.0", "end")
        return "break"

root = tk.Tk()
app = TextToSpeechApp(root)
root.mainloop()

