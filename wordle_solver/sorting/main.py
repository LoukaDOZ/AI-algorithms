import math
import sys

from modules.io import read_words, write_words, read_file, write_file
from modules.info import entropies, H
from modules.waiting import Clock, progress_bar

if __name__ == "__main__":
    words = read_words("../save/word_origin.pl")
    print(f"loaded {len(words)} words")

    sorted_words = []
    clock = Clock()
    clock.start()

    for i, word in enumerate(words):
        sorted_words.append((word, H(words, word)))
        progress_bar(i + 1, len(words), clock, "Calculating H(words)")

    sorted_words = sorted(sorted_words, key=lambda e: e[1], reverse=True)

    writer = write_file("res/sort_info.txt")
    writer.write_elements("Word", "H(Word)")
    for w in sorted_words:
        writer.write_elements(w[0], str(w[1]))
    writer.close()

    write_words("res/sorted_words.pl", [w for w, _ in sorted_words])