# Wordle solver

AI that solves the (french) [Wordle](https://wordle.louan.me/) game using a bank of 7980 (french) words previously sorted by effectivness with the Information Theory.

Information Theory inspirations :
- [ScienceEtonnante](https://www.youtube.com/watch?v=iw4_7ioHWF4)
- [3Blue1Brown](https://www.youtube.com/watch?v=v68zYyaEmEA)

## Project structure

- [`solver.pl`](solver.pl) (solver code)
- [`interactive_play.sh`](interactive_play.sh) (easy interactive way to use the solver)
- [`Makefile`](Makefile)
- [`README.md`](README.md)
- [`sorting/`](sorting/) (sorting algorithm)
    - [`main.c`](sorting/main.c) (sorting algorithm)
    - [`Makefile`](sorting/Makefile)
    - [`README.md`](sorting/README.md)
    - [`source/`](sorting/source/) (static words files)
        - [`words_origin.pl`](sorting/source/words_origin.pl) (original words file)
        - [`words.pl`](sorting/source/words.pl) (best words file from my first sorting algorithm (before rework))
        - [`best.pl`](sorting/source/best.pl) (current best words file) 
    - [`result/`](sorting/result/) (results of the algorithm)

## Usage

Using solver require [Prolog](https://www.swi-prolog.org/).\
Using sorting algortithm requires GCC.

### Makefile

| Command          | Description               |
|------------------|---------------------------|
| `make run`       | Run interactive play      |
| `make install`   | Install Prolog            |
| `make uninstall` | Uninstall Prolog          |
| `make clean`     | Clean all execution files |

### Interactive play

The interactive play is a Bash script running the `solver.pl` script automatically with the `sorting/source/best.pl` words file, suggesting you a word to play each turn and displaying the game in real time.

When it asks you what was the result of the play, enter `g` (green), `o` (orange), `b` (black) for each letters, like : `gobbb`.

The script end when all letters a green, or when 6 turns have passed or when the solver is unable to suggest a word due to constraints (you probably have made a mistake when entering the result).

### Use solver manually

Run Prolog:
```
prolog
```

Once in Prolog, use:
```
consult("solver.pl").
```

The solver automatically imports the words from `sorting/source/best.py`. This can be overwritten with the following (you can ignore the warning message) :
```
consult("path/to/words.pl").
```
#### Main rules

| Rule                     | Description                                                                                                         |
|--------------------------|---------------------------------------------------------------------------------------------------------------------|
| `suggest(P, OS, CS)`     | Suggests a word to play, based on previously played words in `OS` and their coressponding obtained patterns in `CS` |
| `play(S, PS)`            | Simulates a game where `S` is the solution and `PS` all the propositions                                            |
| `success(S)`             | Simulates a game where `S` is the solution tries to find it                                                         |
| `number_of_solutions(N)` | Running a game simulation for each word where it is the solution, calculates the number of success                  |

Words are represented by list of letters like : `[t, a, r, i, e]`. \
Patterns are represented by list of colors like : `[green, orange, black, black, black]`.

### Sorting algorithm

See [sorting/README.md](sorting/README.md).

## Limitations

The first limitation is that the words are sorted before playing the game. For this first turn, it should not be a problem but after that, the information that a word would give may be invalid as some words aren't available anymore. It should update this list in real time based on the state of the game.

Also, it does not distinguish between a common word and an uncommon word. It would be interesting to use word frequency data to favour common words, as they are more likely to be the solution.

## Examples
### Interactive play

```
make
```
**First suggest**

![Capture d’écran du 2024-03-29 14-03-28](https://github.com/LoukaDOZ/AI-algorithms/assets/46566140/86ab75e2-c933-4003-9c0c-735b82022024)

**Game won**

![Capture d’écran du 2024-03-29 14-01-33](https://github.com/LoukaDOZ/AI-algorithms/assets/46566140/d2fc043f-7514-42fe-b0d8-1c4b686b497f)

**In Wordle**

![Capture d’écran du 2024-03-29 14-08-06](https://github.com/LoukaDOZ/AI-algorithms/assets/46566140/48dfe69e-1d17-459f-b4bc-56c4e3e9167b)

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
