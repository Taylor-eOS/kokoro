from pathlib import Path
from audiobook import split_into_chapters, split_chapter_sentences, input_file

NUMBER_WORDS = {
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety", "hundred", "thousand",
}

def main():
    text = Path(input_file).read_text(encoding="utf-8")
    chapters = split_into_chapters(text)
    all_chunks = [split_chapter_sentences(c) for c in chapters]
    total_chunks = sum(len(ch) for ch in all_chunks)
    print(f"Chapters: {len(chapters)}, total chunks: {total_chunks}")
    heading_words = {"chapter", "part", "section", "prologue", "epilogue", "epilog", "introduction", "preface", "interlude"}
    for i, (chap, chunks) in enumerate(zip(chapters, all_chunks), start=1):
        chunk_sizes = [len(c.split()) for c in chunks]
        first_word = chap.split()[0].lower().strip(".,:-") if chap.split() else ""
        is_numeral = first_word.isdigit() or any(first_word.startswith(n) for n in NUMBER_WORDS)
        is_heading = first_word in heading_words or is_numeral
        warning = " ⚠" if not is_heading else ""
        preview = chap[:20].replace("\n", " ")
        print(f"Ch {i:>3}: {len(chunks)} chunks, {chunk_sizes}, {preview!r}{warning}")

if __name__ == '__main__':
    main()
