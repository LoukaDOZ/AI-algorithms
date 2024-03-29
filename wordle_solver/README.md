# Wordle solver

AI that solves the wordle game using a bank of 7980 (french) words previously sorted by effectivness with the Information Theory.

Information Theory inspirations :
- [ScienceEtonnante](https://www.youtube.com/watch?v=iw4_7ioHWF4)
- [3Blue1Brown](https://www.youtube.com/watch?v=v68zYyaEmEA)

## Project structure

- [`solver.pl`](solver.pl) (solver code)
- [`interactive_play.sh`](interactive_play.sh) (easy interactive way to use the solver)
- [`Makefile`](Makefile) (solver code)
- [`README.md`](README.md) (solver code)
- [`save/`](save/) (original words files)
    - [`word_origin.pl`](save/word_origin.pl) (original words file)
    - [`word.pl`](save/word.pl) (best words file from my first sorting algorithm (before rework))
- [`sorting/`](sorting/) (sorting algorithm)
    - [`main.py`](sorting/main.py) (sorting algorithm)
    - [`tests.py`](sorting/tests.py) (tests)
    - [`precalculations.py`](sorting/precalculations.py) (generate pre-calculated data)
    - [`data/`](sorting/data/) (data for calculations)
        - [`precalculated.py`](sorting/data/precalculated.py) (pre-calculated data for calculations speed)
    - [`res/`](sorting/res/) (results of the algorithm)
        - [`sorted_words.pl`](sorting/data/sorted_words.pl) (words sorted by utility for solver)
        - [`sort_info.txt`](sorting/data/sort_info.txt) (sorted words and their information value)
    - [`modules/`](sorting/modules/) (modules for calculations)

## Usage

Using solver require [Prolog](https://www.swi-prolog.org/).\
Using sorting algortithm requires Python.

### Makefile

| Command          | Description          |
|------------------|----------------------|
| `make run`       | Run interactive play |
| `make install`   | Install prolog       |
| `make uninstall` | Uninstall prolog     |

### Interactive play

The interactive play is a Bash script running the `solver.pl` script automatically, suggesting you a word to play each turn and displaying the game in real time. When it asks you what was the result of the play, enter `g` (green), `o` (orange), `b` (black) for each letters, like : `gobbb`.\
The script end when all letters a green, or when 6 turns have passed or when the solver is unable to suggest a word due to constraints (you mostly have made a mistake when entering the result).

### Use solver manually

Run Prolog:
```
prolog
```

Once in Prolog, use:
```
consult("solver.pl").
```

The solver automatically imports the words from `save/word.py`. This can be overwritten with the following (you can ignore the warning message) :
```
consult("path/to/words.pl").
```
#### Main rules

| Rule | Description |
| - | - |
| `suggest(P, OS, CS)` | Suggests a word to play, based on previously played words in `OS` and their coressponding obtained patterns in `CS` |
| `play(S, PS)` | Simulates a game where `S` is the solution and `PS` all the propositions |
| `success(S)` | Simulates a game where `S` is the solution tries to find it |
| `number_of_solutions(N)` | Running a game simulation for each word where it is the solution, calculates the number of success |

Words are represented by list of letters like : `[t, a, r, i, e]`. \
Patterns are represented by list of colors like : `[green, orange, black, black, black]`.

### Sorting algorithm

Place yourself in the `sorting/` folder :
```
cd sorting/
```

Run the pre-calculations if needed :
```
python precalculations.py
```

Run the sorting algoritm :
```
python main.py
```
:warning: Takes approximately 50 minutes to run !

You can know check [`sorted_words.pl`](sorting/data/sorted_words.pl) and [`sort_info.txt`](sorting/data/sort_info.txt).

## Limitations

The first limitation is that the words are sorted before playing the game. For this first turn, it should not be a problem but after that, the information that a word would give may be invalid as some words aren't available anymore. It should update this list in real time based on the state of the game.

Also, it does not distinguish between a common word and an uncommon word. It would be interesting to use word frequency data to favour common words, as they are more likely to be the solution.

## Examples
### Interactive play

```
make run
```

### Manual play

```
prolog
```

```
?- consult("solver.pl").
true.
```

`suggest` :
```
?- suggest(P, [], []).
P = [t, a, r, i, e] .

?- suggest(P, [[t, a, r, i, e]], [[green, orange, black, black, black]]).
P = [t, o, l, a, s].
```

`play` :
```
?- play([t, o, t, a, l], PS).
PS = [[t, o, t, a, l], [t, o, t, a, l], [t, o, t, a, l], [t, o, n, a, l], [t, o, l, a|...], [t, a, r|...]] .
```

`success` :
```
?- success([t, o, t, a, l]).
true .
```

`number_of_solutions` :
```
?- number_of_solutions(N).
N = 7295.
```

### Sorting

```
python precalculations.py
```
```
Generating all 243 possible patterns
Done in 00:00.000
Generating all real patterns
Done in 01:01.576
```

```
python main.py
```
```
loaded 7980 words
[##########] 100.0% (7980/7980) 49:37.659 - Calculating H(words)
```