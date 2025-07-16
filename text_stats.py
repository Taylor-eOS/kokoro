from pathlib import Path
import re
import pysbd
from audiobook import split_into_chapters, split_chapter_sentences, max_sentences_per_audio_file

def statistics(input_file):
    text = Path(input_file).read_text(encoding='utf-8')
    chapters = split_into_chapters(text)
    segmenter = pysbd.Segmenter(language="en", clean=True)
    for chap_idx, chap in enumerate(chapters, 1):
        parts = [p for p in re.split(r'(\n{2,})', chap) if p and not re.match(r'\n{2,}', p)]
        total_sentences = sum(len(segmenter.segment(p.strip())) for p in parts)
        print(f'Chapter {chap_idx}: {total_sentences} sentences total')
        chunks = split_chapter_sentences(chap, max_sentences_per_audio_file)
        for chunk_idx, chunk_text in enumerate(chunks, 1):
            sentences = segmenter.segment(chunk_text.replace('\n\n', ' '))
            words = chunk_text.split()
            print(f'  chunk_{chap_idx}_{chunk_idx} → {len(sentences)} sentences, {len(words)} words')

if __name__ == '__main__':
    statistics('input.txt')
