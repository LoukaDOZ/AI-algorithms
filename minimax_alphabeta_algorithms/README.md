# Minimax and Alphabeta algorithms

AI using MinMax and AlphaBeta algorithms to play to Tic Tac Toe and, by extension, k-in-a-row game.

- [Source project README](aima-python-master/PROJECT.md)
- [See code](aima-python-master/games.py)

<img src="https://github.com/LoukaDOZ/AI-algorithms/assets/46566140/b915d90b-bc67-4a13-b26e-e7b0014f7b68" height="500" />

## Usage

:warning: Require Python.

Launch demo :
```bash
python main.py
```

Arguments:
| Argument    | Description                       | Default        |
| ----------- | --------------------------------- | -------------- |
| --help      | Display help                      |                |
| -w <value>  | Board width                       | 3              |
| -h <value>  | Board height                      | 3              |
| -k <value>  | Number of inlined elements to win | 3              |
| -r          | Choose starting player randomly   | Player1 starts |
| --p1=<type> | Player1 type                      | `query`        |
| --p2=<type> | Player2 type                      | `random`       |

Player types:
| Type        | Description      |
| ----------- | ---------------- |
| `query`     | Human player     |
| `random`    | Random player    |
| `minimax`   | Minimax player   |
| `alphabeta` | Alphabeta player |

(Optional) To use Jupyter notebooks, install following dependencies :
```bash
pip install notebook matplotlib
jupyter notebook
```

Code and algoritm explanations at [aima-python-master/games.ipynb](aima-python-master/games.ipynb) via Jupyter notebook.

## Examples

TicTacToe player vs random:
```bash
python main.py -r
```

TicTacToe player vs player:
```bash
python main.py --p2=query -r
```

TicTacToe random vs alphabeta:
```bash
python main.py --p1=random --p2=alphabeta -r
```

K-in-a-row game:
```bash
python main.py -w 15 -h 15 -k 5 -r
```
