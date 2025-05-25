import os
import re
import random
from pathlib import Path
from generate import generate_audio, save_audio
from pydub import AudioSegment

MAX_CHARS = 4000
INPUT_FILE = 'input.txt'
VOICES = ['af_sky', 'am_eric', 'bf_isabella']
SPEED = 0.95
BASE_PAUSE = 2200

def split_line(text):
    if len(text) <= MAX_CHARS:
        return [text]
    return [text[i:i+MAX_CHARS] for i in range(0, len(text), MAX_CHARS)]
def process_text(text):
    return re.sub(r'\[.*?\]', '', text).replace('*', '_').strip()

def main():
    text = Path(INPUT_FILE).read_text(encoding='utf-8')
    lines = [process_text(line) for line in text.splitlines() if process_text(line)]
    combined = AudioSegment.empty()
    voice_index = 0
    for i, line in enumerate(lines):
        voice = VOICES[voice_index % len(VOICES)]
        voice_index += 1
        for chunk in split_line(line):
            wav = generate_audio(chunk, voice, SPEED)
            wav_path = f"tmp_{i}.wav"
            save_audio(wav, wav_path)
            seg = AudioSegment.from_wav(wav_path)
            os.remove(wav_path)
            if combined:
                combined += AudioSegment.silent(duration=BASE_PAUSE + random.randint(0, 1200))
            combined += seg
    combined.export('shuffled_lines.mp3', format='mp3')

if __name__ == '__main__':
    main()

