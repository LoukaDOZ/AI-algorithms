from modules.pattern import get_pattern, pattern_match, pattern_to_colors, pattern_to_squares
import modules.info as info

assert get_pattern("abaca", "abaca") == "ggggg"
assert get_pattern("abaca", "axxxx") == "gbbbb"
assert get_pattern("abaca", "axaxx") == "gbgbb"
assert get_pattern("abaca", "axaax") == "gbgob"
assert get_pattern("abaca", "qxmoz") == "bbbbb"
assert get_pattern("abaca", "aabaa") == "goobg"
assert get_pattern("abide", "speed") == "bbobo"
assert get_pattern("erase", "speed") == "oboob"

assert pattern_match("abaca", "ggggg", "abaca") == True
assert pattern_match("abaca", "ggggg", "abale") == False
assert pattern_match("abaca", "gggbb", "abale") == True
assert pattern_match("abaca", "gggbb", "abaca") == False
assert pattern_match("abaca", "gggbo", "abaae") == True
assert pattern_match("abaca", "gggbo", "abaac") == False
assert pattern_match("abaca", "gggob", "abaca") == False

print("ggbob --> ", pattern_to_colors("ggbob"), "\n")
print("ggbob -- >", pattern_to_squares("ggbob"), "\n")

all_words = ["abaca", "abale", "abats", "abbes", "abces", "abdos", "abees", "abers", "abeti", "abies", "abima", "abime", "ables", "aboie", "abois", "aboli", "abord", "abots", "about"]
w = "abaca"
pt = "gggbb"
pts = info.get_all_patterns(w)
print(f"Words - len={len(all_words)}:", all_words)
print(f"Patterns('{w}'):", pts)
print(f"Count matches({pattern_to_colors(pt)}):", info.count_matches(all_words, w, pt))
print(f"p({pattern_to_colors(pt)}):", info.p(all_words, w, pt))
print(f"I({pattern_to_colors(pt)}):", info.I(all_words, w, pt, info.p(all_words, w, pt)))
print(f"H('{w}'):", info.H(all_words, w))
print("Entropies:", sorted(info.entropies(all_words), key=lambda e: e[1], reverse=True))
print()

print("Success !")