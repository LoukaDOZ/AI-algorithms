import sys
import random

sys.path.append('aima-python-master/')

from games import random_player, minimax_player, alphabeta_player
from mygame import CustomGame, CustomPlayer, custom_query_player

def validate_player(p):
    return p == "query" or p == "random" or p == "minimax" or p == "alphabeta"

def str_player_to_fnc(p):
    if p == "query":
        return custom_query_player
    
    if p == "random":
        return random_player
    
    if p == "minimax":
        return minimax_player
    
    if p == "alphabeta":
        return alphabeta_player
    
    return None

def get_args():
    filename = sys.argv[0]
    options = {
        "w": 3,
        "h": 3,
        "win_count": 3,
        "rand_start": False,
        "p1": "query",
        "p2": "random"
    }

    count = 1
    while count < len(sys.argv):
        arg = sys.argv[count]

        if arg == "--help":
            print(f"Usage: {filename} <options>")

            print("\nOptions:")
            print("--help\t\tDisplay this help message")
            print("-w\t\tBoard width (default: 3)")
            print("-h\t\tBoard height (default: 3)")
            print("-k\t\tNumber of inlined elements to win (default: 3)")
            print("-r\t\tChoose starting player randomly (default: always Player1)")
            print("--p1=<type>\tPlayer 1 type (default: query)")
            print("--p2=<type>\tPlayer 2 type (default: random)")

            print("\nPlayer types:")
            print("query\t\tHuman player")
            print("random\t\tRandom player")
            print("minimax\tMinimax player")
            print("alphabeta\tAlphabeta player")
            return None
        elif arg == "-h":
            v = int(sys.argv[count + 1])
            if v < 1:
                print("Invalid value for -h : ", v, file=sys.stderr)
                print(f"For help, use: {filename} --help ", file=sys.stderr)
                return None

            options["h"] = v
            count +=1
        elif arg == "-w":
            v = int(sys.argv[count + 1])
            if v < 1:
                print("Invalid value for -w : ", v, file=sys.stderr)
                print(f"For help, use: {filename} --help ", file=sys.stderr)
                return None

            options["w"] = v
            count +=1
        elif arg == "-k":
            v = int(sys.argv[count + 1])
            if v < 1:
                print("Invalid value for -k : ", v, file=sys.stderr)
                print(f"For help, use: {filename} --help ", file=sys.stderr)
                return None

            options["win_count"] = v
            count +=1
        elif arg == "-r":
            options["rand_start"] = True
        elif arg.startswith("--p1="):
            v = arg[5:]
            if not validate_player(v):
                print("Invalid value for -p1 : ", v, file=sys.stderr)
                print(f"For help, use: {filename} --help ", file=sys.stderr)
                return None

            options["p1"] = v
        elif arg.startswith("--p2="):
            v = arg[5:]
            if not validate_player(v):
                print("Invalid value for -p2 : ", v, file=sys.stderr)
                print(f"For help, use: {filename} --help ", file=sys.stderr)
                return None

            options["p2"] = v
        else:
            print(f"Unknown argument : {arg}", file=sys.stderr)
    
        count += 1
    
    return options

if __name__ == "__main__":
    options = get_args()
    if options is None:
        exit(1)

    game = CustomGame(options["w"], options["h"], options["win_count"])
    players = [
        CustomPlayer("Player1", options["p1"], str_player_to_fnc(options["p1"])),
        CustomPlayer("Player2", options["p2"], str_player_to_fnc(options["p2"]))
    ]

    if(options["rand_start"]):
        random.shuffle(players)

    game.play_game(*players)