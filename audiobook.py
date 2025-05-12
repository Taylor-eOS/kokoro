import os
import re
import math
import pysbd
from pathlib import Path
from generate import generate_audio, save_audio
from pydub import AudioSegment

MAX_CHARS = 4000
INPUT_FILE = 'input.txt'
LOG_FILE = 'chunks.txt'
TEST = False
segmenter = pysbd.Segmenter(language='en', clean=False)
AUDIOBOOK_VOICE = 'am_eric'
AUDIOBOOK_SPEED = 1.15

def split_into_chapters(text):
    parts = re.split(r'\n\s*\n+', text.strip())
    return [p.strip() for p in parts if p.strip()]

def split_chapter_sentences(chap):
    PARAGRAPH_PLACEHOLDER = "||PARAGRAPH||"
    paragraph_breaks = re.split(r'(\n{2,})', chap)
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
    return ["".join(processed).strip()]

def main():
    text = Path(INPUT_FILE).read_text(encoding='utf-8')
    chapters = split_into_chapters(text)
    idx = 1
    for chap in chapters:
        for chunk in split_chapter_sentences(chap):
            if TEST:
                with open(LOG_FILE, "a") as f:
                    f.write(f"Chunk {idx}: {chunk}\n\n")
            else:
                wav_path = f"chunk_{idx}.wav"
                #audio = generate_audio(chunk)
                audio = generate_audio(chunk, AUDIOBOOK_VOICE, AUDIOBOOK_SPEED)
                save_audio(audio, wav_path)
                mp3_path = f"chunk_{idx}.mp3"
                AudioSegment.from_wav(wav_path).export(mp3_path, format='mp3')
                try:
                    os.remove(wav_path)
                except FileNotFoundError:
                    print(f"Error removing wav file: {wav_path}")
            idx += 1

if __name__ == '__main__':
    try:
        os.remove(LOG_FILE)
    except FileNotFoundError:
        pass
    main()

