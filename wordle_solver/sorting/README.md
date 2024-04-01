# Sorting algortihm

Algorithm to sort words by the average information they could bring with the Information Theory to solve Wordle.

## Usage

| Command      | Description                       |
|--------------|-----------------------------------|
| `make run`   | Compile and run sorting algorithm |
| `make build` | Compile sorting algorithm         |
| `make clean` | Clean all execution files         |

### Manual run

```
make build
./exec <options>
```

Options:
| Argument                | Description                              | Default                  |
|-------------------------|------------------------------------------|--------------------------|
| `-h, --help`            | Display help message                     |                          |
| `--quiet`               | Hide execution messages                  |                          |
| `--test`                | Run tests                                |                          |
| `-i, --input <file>`    | Path to words source file (Prolog file)  | `source/words_origin.pl` |
| `-o, --output <folder>` | Path to folder where to put result files | `result/`                |

### Execution results

After the execution, 2 files a created in the output folder :
- `words.pl` (words sorted by utility for solver)
- `words_info.txt` (sorted words and their entropy value)