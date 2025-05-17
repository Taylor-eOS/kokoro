import os
import re
from pathlib import Path
import pysbd
from generate import generate_audio, save_audio
from pydub import AudioSegment

MAX_CHARS = 4000
INPUT_FILE = 'input.txt'
LOG_FILE = 'chunks.txt'
TEST = False
USER_VOICE = 'am_eric'
ASSISTANT_VOICE = 'bf_isabella'
SPEED = 1.15
PAUSE = 400

segmenter = pysbd.Segmenter(language='en', clean=False)

def split_sentences(text):
    PAR = "||PAR||"
    parts = re.split(r'(\n{2,})', text)
    elems = []
    for p in parts:
        if not p: continue
        if re.match(r'\n{2,}', p):
            elems.append(PAR)
        else:
            elems.extend(segmenter.segment(p.strip()))
    chunks, buf = [], ''
    for e in elems:
        if e == PAR:
            if buf: chunks.append(buf.strip()); buf = ''
            chunks.append('') 
        else:
            if len(buf) + len(e) + 1 > MAX_CHARS:
                chunks.append(buf.strip())
                buf = e + ' '
            else:
                buf += e + ' '
    if buf: chunks.append(buf.strip())
    return [c for c in chunks if c is not None]

def parse_turns(text):
    raw = re.split(r'(?m)^---\s*$', text.strip())
    turns = []
    for section in raw:
        lines = section.strip().splitlines()
        if not lines: continue
        label = lines[0].rstrip(':').strip()
        content = '\n'.join(lines[1:]).strip()
        if content:
            turns.append((label, content))
    return turns

def strip_bracketed(text):
    return re.sub(r'\[.*?\]', '', text)

def main():
    text = Path(INPUT_FILE).read_text(encoding='utf-8')
    turns = parse_turns(text)
    combined = AudioSegment.empty()
    prev_label = None
    idx = 1
    for label, content in turns:
        voice = USER_VOICE if label.lower() == 'user' else ASSISTANT_VOICE
        chunks = [content] if len(content) <= MAX_CHARS else split_sentences(content)
        for chunk in chunks:
            clean_chunk = strip_bracketed(chunk).strip()
            if not clean_chunk:
                continue
            if TEST:
                with open(LOG_FILE, 'a') as f:
                    f.write(f"Chunk {idx}: [{label}] {clean_chunk}\n\n")
            else:
                wav = generate_audio(clean_chunk, voice, SPEED)
                wav_path = f"tmp_{idx}.wav"
                save_audio(wav, wav_path)
                seg = AudioSegment.from_wav(wav_path)
                os.remove(wav_path)

                if prev_label is None:
                    combined += seg
                else:
                    pause = PAUSE if label != prev_label else PAUSE/2
                    combined += AudioSegment.silent(duration=pause) + seg

                prev_label = label
            idx += 1
    if not TEST:
        combined.export('combined.mp3', format='mp3')

if __name__ == '__main__':
    try: os.remove(LOG_FILE)
    except FileNotFoundError: pass
    main()

