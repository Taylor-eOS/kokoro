import os
import re
import math
import pysbd
from pathlib import Path

input_file = 'input.txt'
log_file = 'chunks.txt'
test_mode_on = False
default_language = 'en'
default_language = input(f"Speaker language ({default_language}): ") or default_language
segmenter = pysbd.Segmenter(language=default_language, clean=False)
speaker_voices = ['bf_isabella', 'af_heart', 'am_michael', 'af_sky', 'am_adam', 'af_nova', 'af_alloy']
speaker_voice = speaker_voices[0]
speaker_voice_speed = 1.0
max_sentences_per_audio_file = 140
offset = int(input("Chapter index offset (-1 = prologue): ") or 1)

#load models after startup
from generate import generate_audio, save_audio
from pydub import AudioSegment

def select_speaker_voice():
    for index, voice in enumerate(speaker_voices, 1):
        print(f"{index}. {voice}")
    while True:
        choice = input(f"Speaker voice, number or name ({speaker_voice}): ").strip()
        if not choice:
            return speaker_voice
        if choice.isdigit() and 1 <= int(choice) <= len(speaker_voices):
            return speaker_voices[int(choice) - 1]
        if choice in speaker_voices:
            return choice
        print("Invalid selection")

speaker_voice = select_speaker_voice()

def split_into_chapters(text):
    parts = re.split(r'\n\s*\n+', text.strip())
    return [p.strip() for p in parts if p.strip()]

def split_chapter_sentences(chap, max_sentences=max_sentences_per_audio_file):
    paragraphs = [p.strip() for p in chap.split('\n\n') if p.strip()]
    sentences = [s for p in paragraphs for s in segmenter.segment(p)]
    total = len(sentences)
    num_chunks = max(1, math.ceil(total / max_sentences))
    target = total / num_chunks
    chunks = []
    current = []
    for i, s in enumerate(sentences):
        current.append(s)
        if len(chunks) < num_chunks - 1 and i + 1 >= round(target * (len(chunks) + 1)):
            chunks.append(' '.join(current))
            current = []
    if current:
        chunks.append(' '.join(current))
    return chunks

def main():
    print(f"Speaker voice: {speaker_voice}")
    text = Path(input_file).read_text(encoding='utf-8')
    chapters = split_into_chapters(text)
    for chap_idx, chap in enumerate(chapters, 1):
        chunks = split_chapter_sentences(chap)
        for chunk_idx, chunk in enumerate(chunks, 1):
            chapter_number = chap_idx + offset
            label = f"{chapter_number:02d}-{chunk_idx}"
            if test_mode_on:
                with open(log_file, "a") as f:
                    f.write(f"Chunk {label}: {chunk}\n\n")
            else:
                wav_path = f"chunk_{label}.wav"
                audio = generate_audio(chunk, speaker_voice, speaker_voice_speed)
                save_audio(audio, wav_path)
                mp3_path = f"chunk_{label}.mp3"
                AudioSegment.from_wav(wav_path).export(mp3_path, format='mp3')
                try:
                    os.remove(wav_path)
                except FileNotFoundError:
                    print(f"Error removing wav file: {wav_path}")

if __name__ == '__main__':
    try:
        os.remove(log_file)
    except FileNotFoundError:
        pass
    main()
