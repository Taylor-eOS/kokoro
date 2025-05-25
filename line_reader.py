import os
import re
from pathlib import Path
from generate import generate_audio, save_audio
from pydub import AudioSegment

MAX_CHARS = 4000
INPUT_FILE = 'input.txt'
LOG_FILE = 'chunks.txt'
TEST = False
VOICES = ['af_sky', 'am_eric', 'bf_isabella']
SPEED = 0.95
PAUSE = 1800

def split_line(text, max_chars):
    if len(text) <= max_chars:
        return [text]
    chunks = []
    current_chunk = []
    current_length = 0
    words = text.split()
    for word in words:
        if current_length + len(word) + 1 > max_chars:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_length = 0
            while len(word) > max_chars:
                chunks.append(word[:max_chars])
                word = word[max_chars:]
            if word:
                current_chunk.append(word)
                current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def strip_bracketed(text):
    text = re.sub(r'\[.*?\]', '', text)
    return text.replace('*', '_')

def main():
    text = Path(INPUT_FILE).read_text(encoding='utf-8')
    lines = [line.strip() for line in text.splitlines()]
    non_empty_lines = [line for line in lines if line]
    combined = AudioSegment.empty()
    prev_voice = None
    voice_index = 0
    idx = 1
    for line in non_empty_lines:
        clean_line = strip_bracketed(line).strip()
        if not clean_line:
            continue
        voice = VOICES[voice_index % len(VOICES)]
        voice_index += 1
        chunks = split_line(clean_line, MAX_CHARS)
        for chunk in chunks:
            if TEST:
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(f"Chunk {idx}: [{voice}] {chunk}\n\n")
            else:
                wav = generate_audio(chunk, voice, SPEED)
                wav_path = f"tmp_{idx}.wav"
                save_audio(wav, wav_path)
                seg = AudioSegment.from_wav(wav_path)
                os.remove(wav_path)
                if prev_voice is None:
                    combined += seg
                else:
                    pause = PAUSE if voice != prev_voice else PAUSE // 2
                    combined += AudioSegment.silent(duration=pause) + seg
                prev_voice = voice
            idx += 1
    if not TEST:
        combined.export('combined.mp3', format='mp3')

if __name__ == '__main__':
    try:
        os.remove(LOG_FILE)
    except FileNotFoundError:
        pass
    main()

