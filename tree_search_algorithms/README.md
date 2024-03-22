# Tree search algorithms

[See code](./code.c)

Some tree search algorithms to solve a fifteen puzzle game such as :
- Breadth-first search
- Depth-first search
- Depth limited search
- Iterative deepening search
- A* algorithm

## Usage

```bash
gcc -o exec code.c
./exec <options>
```

Options:
| Argument         | Description                                                                          | Default      | Min | Max     |
| ---------------- | ------------------------------------------------------------------------------------ | ------------ | --- | ------- |
| -r <number>      | Number of random moves to shuffle board                                              | 100          | 0   | INT_MAX |
| -d <max depth>   | Maximum depth for depth limited search search                                                 | 20           | 0   | INT_MAX |
| -b <start board> | Start board. Usage: 9 numbers each different from 0 to 8, where 0 represent the hole | 012345678    |     |         |
| -i               | Print a line every time a new depth is reached                                       | Not printed  |     |         |
| -bf              | Breadth-first search algorithm                                                       | Not executed |     |         |
| -df              | Depth-first search algorithm                                                         | Not executed |     |         |
| -dl              | Depth limited search algorithm                                                       | Not executed |     |         |
| -id              | Iterative deepening search algorithm                                                 | Not executed |     |         |
| -a               | A* algorithm                                                                         | Not executed |     |         |

If none of these arguments are given : `-bf`, `-df`, `-dl`, `-id`, `-a`, all arlgorithms are executed.

## Examples

```bash
./exec -r 50
```
```
========== Start board (50 random movements) ==========
+---+---+---+
| 3 | 7 |   |
+---+---+---+
| 4 | 2 | 1 |
+---+---+---+
| 6 | 8 | 5 |
+---+---+---+

========== Breadth-first search ==========

Win configuration found a depth : 10
Number of moves to win : 10
Treated nodes : 651
Time : 0.014147 seconds

========== Depth-first search ==========

Win configuration found a depth : 108742
Number of moves to win : 108742
Treated nodes : 119697
Time : 57.894257 seconds

========== Depth limited search (max depth = 20) ==========

Win configuration found a depth : 20
Number of moves to win : 20
Treated nodes : 8959
Time : 0.524414 seconds

========== Iterative deepening search ==========

========== Iterative deepening search (max depth = 1) ==========
Treated nodes : 3

========== Iterative deepening search (max depth = 2) ==========
Treated nodes : 7

========== Iterative deepening search (max depth = 3) ==========
Treated nodes : 15

========== Iterative deepening search (max depth = 4) ==========
Treated nodes : 31

========== Iterative deepening search (max depth = 5) ==========
Treated nodes : 51

========== Iterative deepening search (max depth = 6) ==========
Treated nodes : 90

========== Iterative deepening search (max depth = 7) ==========
Treated nodes : 153

========== Iterative deepening search (max depth = 8) ==========
Treated nodes : 273

========== Iterative deepening search (max depth = 9) ==========
Treated nodes : 437

========== Iterative deepening search (max depth = 10) ==========
Treated nodes : 160

Win configuration found a depth : 10
Number of moves to win : 10
Treated nodes : 1220
Time : 0.001516 seconds

========== A* algorithm (heuristic = h1) ==========

Win configuration found a depth : 10
Number of moves to win : 10
Treated nodes : 28
Time : 0.000020 seconds

========== A* algorithm (heuristic = h2) ==========

Win configuration found a depth : 10
Number of moves to win : 10
Treated nodes : 21
Time : 0.000024 seconds

========== A* algorithm (heuristic = h3) ==========

Win configuration found a depth : 26
Number of moves to win : 26
Treated nodes : 148
Time : 0.000307 seconds
```

```bash
./exec -b 876543210 -d 15 -i -dl
```
```
========== Start board (100 random movements) ==========
+---+---+---+
| 8 | 5 | 7 |
+---+---+---+
|   | 2 | 6 |
+---+---+---+
| 4 | 1 | 3 |
+---+---+---+

========== Depth limited search (max depth = 15) ==========
New depth reached : 0
New depth reached : 1
New depth reached : 2
New depth reached : 3
New depth reached : 4
New depth reached : 5
New depth reached : 6
New depth reached : 7
New depth reached : 8
New depth reached : 9
New depth reached : 10
New depth reached : 11
New depth reached : 12
New depth reached : 13
New depth reached : 14
New depth reached : 15

Win configuration not found
Treated nodes : 10157
Time : 0.617346 seconds
```