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

def split_into_chapters(text):
    parts = re.split(r'\n\s*\n+', text.strip())
    return [p.strip() for p in parts if p.strip()]

def split_chapter_sentences(chapter):
    sentences = [s.strip() for s in segmenter.segment(chapter) if s.strip()]
    total_chars = sum(len(s) for s in sentences)
    num_chunks = max(1, min(len(sentences), math.ceil(total_chars / MAX_CHARS)))
    target = total_chars / num_chunks
    chunks, current, curr_len = [], [], 0
    for s in sentences:
        if curr_len + len(s) > target and len(chunks) < num_chunks - 1:
            chunks.append(' '.join(current))
            current, curr_len = [s], len(s)
        else:
            current.append(s)
            curr_len += len(s)
    chunks.append(' '.join(current))
    return chunks

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
                audio = generate_audio(chunk)
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

