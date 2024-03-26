import sys
import time

sys.path.append('aima-python-master/')

from games import TicTacToe, GameState

def custom_query_player(game, state):
    actions = game.actions(state)
    print("available moves: {}".format(actions))
    print("")

    move = None
    while True:
        move_string = input('Your move ? ')
        try:
            move = eval(move_string)
            if type(move) == tuple and len(move) == 2 and move in actions:
                break
        except Exception:
            pass
    return move

class CustomPlayer():
    def __init__(self, name, func_name, func):
        self.name = name
        self.func_name = func_name
        self.func = func

class CustomGame(TicTacToe):
    BLUE = 'X'
    RED = 'O'

    def __init__(self, h, v, k):
        super().__init__(h, v, k)
    
    def __blue__(self, s):
        return f"\033[34m{s}\033[37m"
    
    def __red__(self, s):
        return f"\033[31m{s}\033[37m"
    
    def __yellow__(self, s):
        return f"\033[33m{s}\033[37m"
    
    def __color__(self, s, symbol):
        if symbol == CustomGame.BLUE:
            return self.__blue__(s)
        
        if symbol == CustomGame.RED:
            return self.__red__(s)
        
        return s
    
    def __get_k_len_lines__(self, board, x, y):
        k_lines = []

        if x - (self.k - 1) >= 1:
            k_lines.append([(x - i, y) for i in range(self.k)])

        if x + self.k - 1 <= self.h:
            k_lines.append([(x + i, y) for i in range(self.k)])
        
        if y - (self.k - 1) >= 1:
            k_lines.append([(x, y - i) for i in range(self.k)])

        if y + self.k - 1 <= self.v:
            k_lines.append([(x, y + i) for i in range(self.k)])
        
        if x - (self.k - 1) >= 1 and y - (self.k - 1) >= 1:
            k_lines.append([(x - i, y - i) for i in range(self.k)])
        
        if x - (self.k - 1) >= 1 and y + self.k - 1 <= self.v:
            k_lines.append([(x - i, y + i) for i in range(self.k)])

        if x + self.k - 1 <= self.h and y - (self.k - 1) >= 1:
            k_lines.append([(x + i, y - i) for i in range(self.k)])

        if x + self.k - 1 <= self.h and y + self.k - 1 <= self.v:
            k_lines.append([(x + i, y + i) for i in range(self.k)])
        
        return k_lines

    def __get_win_line__(self, state, player):
        board = state.board
        k_len_lines = []
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                if board.get((x, y)) == player:
                    for k_line in self.__get_k_len_lines__(board, x, y):
                        win = True

                        for c in k_line:
                            if board.get(c) != player:
                                win = False
                                break
                        
                        if win:
                            return k_line

    def __display_win__(self, state, player):
        line = self.__get_win_line__(state, player)
        
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                s = board.get((x, y), '.')

                if (x, y) in line:
                    s = self.__color__(s, s)
                
                print(s, end=' ')
            print()

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                s = board.get((x, y), '.')
                print(self.__color__(s, s), end=' ')
            print()
    
    def play_game(self, *players):
        print("==== START GAME ====")
        print(f"{self.__blue__(players[0].name)} ({players[0].func_name}) VS {self.__red__(players[1].name)} ({players[1].func_name})")
        print(f"{self.__blue__(players[0].name)} STARTS")
        self.display(self.initial)
        print()

        state = self.initial
        run = True
        turn = 1
        while run:
            for player in players:
                print("----- Turn", turn, "-----")

                move = player.func(self, state)
                print(f"{self.__color__(player.name, state.to_move)} has played {move}")
                
                state = self.result(state, move)
                self.display(state)
                print()   

                if self.terminal_test(state):
                    run = False
                    break
                
                turn += 1
                time.sleep(0.7)
        
        final_result = self.utility(state, self.to_move(self.initial))
        
        print("==== GAME FINISHED ====")
        if final_result == 0:
            print(self.__yellow__("TIE !"))
        else:
            player = players[0 if final_result > 0 else 1]
            symbol = CustomGame.BLUE if final_result > 0 else CustomGame.RED
            print(self.__color__(player.name, symbol), self.__yellow__("HAS WON !"))
            self.__display_win__(state, symbol)