import math

from modules.pattern import pattern_match
from data.precalculated import all_real_patterns

def get_all_patterns(word):
    return all_real_patterns[word]

def count_matches(all_words, word, pattern):
    return len([None for w in all_words if pattern_match(word, pattern, w)])

def p(all_words, word, pattern):
    return count_matches(all_words, word, pattern) / len(all_words)

def I(all_words, word, pattern, probability):
    if probability == 0:
        return 0

    return math.log2(1 / probability)

def H(all_words, word):
    _sum = 0

    for pattern in get_all_patterns(word):
        probability = p(all_words, word, pattern)
        _sum += probability * I(all_words, word, pattern, probability)
    
    return _sum

def entropies(words):
    return [(w, H(words, w)) for w in words]