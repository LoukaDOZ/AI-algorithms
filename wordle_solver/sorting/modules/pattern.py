def get_pattern(soluce, proposition):
    pattern = ['b' for _ in proposition]
    unset = []

    for i, l in enumerate(proposition):
        if l == soluce[i]:
            pattern[i] = 'g'
        else:
            unset.append(soluce[i])
    
    for i, l in enumerate(proposition):
        if pattern[i] != 'b':
            continue
        
        if l in unset:
            pattern[i] = 'o'
            unset.remove(l)
    
    return "".join(pattern)

def pattern_match(word, pattern, match):
    matchl = list(match)

    for i, p in enumerate(pattern):
        if p != 'g':
            continue

        if match[i] != word[i]:
            return False
        
        matchl[i] = None
    
    for i, p in enumerate(pattern):
        if p != 'o':
            continue

        found = -1

        for j, l in enumerate(matchl):
            if l is None or i == j:
                continue

            if l == word[i]:
                found = j
                break
        
        if found == -1:
            return False
        
        matchl[found] = None
    
    for i, p in enumerate(pattern):
        if p != 'b':
            continue
        
        if word[i] in matchl:
            return False
    
    return True

def pattern_to_colors(pattern):
    pattern = pattern.replace('g', "\033[32mg\033[37m")
    pattern = pattern.replace('o', "\033[33mo\033[37m")
    pattern = pattern.replace('b', "\033[30mb\033[37m")
    return pattern

def pattern_to_squares(pattern):
    pattern = pattern.replace('g', "🟩")
    pattern = pattern.replace('o', "🟨")
    pattern = pattern.replace('b', "⬛")
    return pattern