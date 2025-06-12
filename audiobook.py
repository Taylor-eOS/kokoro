import os
import re
import pysbd
from pathlib import Path
from generate import generate_audio, save_audio
from pydub import AudioSegment

input_file = 'input.txt'
log_file = 'chunks.txt'
test_mode_on = False
segmenter = pysbd.Segmenter(language='en', clean=False)
speaker_voice = 'am_michael'
speaker_voice_speed = 1.0
max_sentences_per_audio_file = 120

def split_into_chapters(text):
    parts = re.split(r'\n\s*\n+', text.strip())
    return [p.strip() for p in parts if p.strip()]

def split_chapter_sentences(chap, max_sentences=max_sentences_per_audio_file):
    paragraph_placeholder = "||PARAGRAPH||"
    paragraph_breaks = re.split(r'(\n{2,})', chap)
    segmenter = pysbd.Segmenter(language="en", clean=True)
    elements = []
    for part in paragraph_breaks:
        if not part:
            continue
        if re.match(r'\n{2,}', part):
            elements.append(paragraph_placeholder)
        else:
            elements.extend(segmenter.segment(part.strip()))
    processed = []
    for el in elements:
        if el == paragraph_placeholder:
            processed.append("\n\n")
        else:
            processed.append(el + "\n\n")
    chunks = [processed[i:i+max_sentences] for i in range(0, len(processed), max_sentences)]
    if len(chunks) > 1:
        a, b = chunks[-2], chunks[-1]
        combined = a + b
        half = len(combined) // 2
        chunks[-2], chunks[-1] = combined[:half], combined[half:]
    return ["".join(chunk).strip() for chunk in chunks]

def main():
    text = Path(input_file).read_text(encoding='utf-8')
    chapters = split_into_chapters(text)
    idx = 1
    for chap in chapters:
        for chunk in split_chapter_sentences(chap):
            if test_mode_on:
                with open(log_file, "a") as f:
                    f.write(f"Chunk {idx}: {chunk}\n\n")
            else:
                wav_path = f"chunk_{idx}.wav"
                audio = generate_audio(chunk, speaker_voice, speaker_voice_speed)
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
        os.remove(log_file)
    except FileNotFoundError:
        pass
    main()

