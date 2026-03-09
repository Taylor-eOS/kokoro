import os
import re
import math
import pysbd
from pathlib import Path
from generate import generate_audio, save_audio
from pydub import AudioSegment

input_file = 'input.txt'
log_file = 'chunks.txt'
test_mode_on = False
segmenter = pysbd.Segmenter(language='en', clean=False)
speaker_voice = 'am_echo' #'am_onyx' #'am_adam' #'af_heart' #'am_michael'
speaker_voice_speed = 1.0
max_sentences_per_audio_file = 140

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

