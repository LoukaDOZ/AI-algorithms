"""Games, or Adversarial Search (Chapter 5)"""
from collections import namedtuple
import random

from utils import argmax

infinity = float('inf')
GameState = namedtuple('GameState', 'to_move, utility, board, moves')

# ______________________________________________________________________________
# III - Création d’une fonction d’évaluation

# ______________________________________________________________________________
# Q1/ Fonction fEval
def fEval_1(state, player):
    opponent = 'O'
    if player == 'O':
        opponent = 'X'

    score = 0
    lines = [
        [(1, 1), (1, 2), (1, 3)], [(2, 1), (2, 2), (2, 3)], [(3, 1), (3, 2), (3, 3)], # Lignes
        [(1, 1), (2, 1), (3, 1)], [(1, 2), (2, 2), (3, 2)], [(1, 3), (2, 3), (3, 3)], # Colonnes
        [(1, 1), (2, 2), (3, 3)], [(1, 3), (2, 2), (3, 1)] # Diagonales
   ]

    # Pour chaque ligne, chaque colonne et chaque diagonale
    board = state.board
    for i in lines:
        plyCount = 0
        oppCount = 0

        for j in i:
            if board.get(j, '.') == player:
                plyCount += 1
            elif board.get(j, '.') == opponent:
                oppCount += 1

        # Si 1 pion allié : +1
        if plyCount == 1 and oppCount == 0:
            score += 1
        # Si 1 pion adverse : -1
        elif plyCount == 0 and oppCount == 1:
            score -= 1
        # Si 2 pions alliés : +3
        elif plyCount == 2 and oppCount == 0:
            score += 3
        # Si 2 pions adverses : -3
        elif plyCount == 0 and oppCount == 2:
            score -= 3
        # Si au moins 1 pion allié et 1 au moins 1 pion adverse : ne rien faire (+0)

    return score

# ______________________________________________________________________________
# IV – Elagage maximum

# ______________________________________________________________________________
# Q1/ Ordonnancement des noeuds
# descending = True (ordre décroissant) pour max_value()
# descending = False (ordre croissant) pour min_value()
def sortState_1(state, game, player, descending):
    def sortKey(e):
        return e[0]

    # Evaluer avec fonction fEval si non terminal, sinon avec utility
    def evalState(s):
        if game.terminal_test(s):
            return game.utility(s, player)

        return fEval_1(s, player)

    sort = []
    for a in game.actions(state):
        sort.append((evalState(game.result(state, a)), a))
    sort.sort(key = sortKey, reverse = descending)

    return [x[1] for x in sort]

# ______________________________________________________________________________
# V – Etendre le jeu à un damier plus grand.

# ______________________________________________________________________________
# Q1/ Fonction sortState qui utilise fEval2() au lieu de fEval_1()
def sortState_2(state, game, player, descending):
    def sortKey(e):
        return e[0]

    # Evaluer avec fonction fEval si non terminal, sinon avec utility
    def evalState(s):
        if game.terminal_test(s):
            return game.utility(s, player)

        return fEval_2(s, player, game)

    sort = []
    for a in game.actions(state):
        sort.append((evalState(game.result(state, a)), a))
    sort.sort(key = sortKey, reverse = descending)

    return [x[1] for x in sort]

# ______________________________________________________________________________
# Q1/ Fonction fEval pour damier de taille w x h (w = nombre colonnes, h = nombre lignes) avec k coups pour gagner
# /!\ Ne marche que si v >= k et h >= k
def fEval_2(state, player, game):
    w = game.v
    h = game.h
    k = game.k

    opponent = 'O'
    if player == 'O':
        opponent = 'X'

    lines = []

    # Génération des lignes, colonnes et diagonales a vérifier
    for x in range(1, h + 1):
        for y in range(1, w + 1):
            # Lignes
            # Gauche à droite
            # Ne pas faire si < de k - 1 colonnes a droite de la case actuelle
            if y + k - 1 <= w:
                l = []
                for i in range(0, k):
                    l.append((x, y + i))
                lines.append(l)
            # Colonnes
            # Haut en bas
            # Ne pas faire si < de k - 1 lignes en bas de la case actuelle
            if x + k - 1 <= h:
                l = []
                for i in range(0, k):
                    l.append((x + i, y))
                lines.append(l)
            # Diagonales gauche à droite
            # Ne pas faire si < de k - 1 colonnes a droite de la case actuelle
            # Ne pas faire si < de k - 1 lignes en bas de la case actuelle
            if x + k - 1 <= h and y + k - 1 <= w:
                l = []
                for i in range(0, k):
                    l.append((x + i, y + i))
                lines.append(l)
            # Diagonales droite à gauche
            # Ne pas faire si < de k - 1 colonnes a gauche de la case actuelle
            # Ne pas faire si < de k - 1 lignes en bas de la case actuelle
            if x + k - 1 <= h and y - (k - 1) > 0:
                l = []
                for i in range(0, k):
                    l.append((x + i, y - i))
                lines.append(l)

    # Pour chaque ligne, chaque colonne et chaque diagonale
    board = state.board
    score = 0
    for i in lines:
        plyCount = 0
        oppCount = 0

        for j in i:
            if board.get(j, '.') == player:
                plyCount += 1
            elif board.get(j, '.') == opponent:
                oppCount += 1

        if plyCount == k - 1 and oppCount == 0:
            score += 1
        elif plyCount == 0 and oppCount == k - 1:
            score -= 1
        elif plyCount >= 1 and oppCount == 0:
            score += 1 * (10 ** (plyCount - k))
        elif plyCount == 0 and oppCount >= 1:
            score -= 1 * (10 ** (oppCount - k))

    return round(score, k)

from games import *

# ______________________________________________________________________________
# III - Création d’une fonction d’évaluation

# ______________________________________________________________________________
# Q1/ Tests de la fonction fEval_1()
def tests_fEval_1():
    game = TicTacToe()
    testCases = [
        {
            "pos": [(1,1)],
            "expectedX": 3
        },
        {
            "pos": [(2,2), (1,2)],
            "expectedX": 2
        },
        {
            "pos": [(1,1), (2,1), (1,2), (2,2), (2,3), (3,2), (3,3)],
            "expectedX": 5
        },
        {
            "pos": [(1,1), (1,3), (1,2), (2,2), (2,1), (3,2), (2,3)],
            "expectedX": -1
        },
        {
            "pos": [(1,1), (1,3), (3,1), (3,3)],
            "expectedX": 0
        }
    ]

    for i,t in enumerate(testCases):
        ttt = game.initial

        for p in t["pos"]:
            ttt = game.result(ttt, p)

        print("=== Test ", i, " ===")
        game.display(ttt)

        for p in "XO":
            expected = t["expectedX"]
            if p == 'O':
                expected = -expected

            feval = fEval_1(ttt, p)
            print("Résultat attendu pour ", p, " : ", expected, " | Obtenu : ", feval, " -> ", end="")

            if feval == expected:
                print("OK !")
            else:
                print("Non OK !")
        print()

# ______________________________________________________________________________
# IV – Elagage maximum

# ______________________________________________________________________________
# Q1/ Tests de la fonction sortState_1()
def tests_sortState_1():
    def evalState(s, p):
        if game.terminal_test(s):
            return game.utility(s, p)

        return fEval_1(s, p)

    game = TicTacToe()
    testCases = [
        {
            "pos": []
        },
        {
            "pos": [(1,1)]
        },
        {
            "pos": [(2,2), (1,2)]
        },
        {
            "pos": [(1,1), (2,1), (1,2), (2,2), (2,3), (3,2), (3,3)]
        },
        {
            "pos": [(1,1), (1,3), (3,1), (3,3)]
        }
    ]

    for i,t in enumerate(testCases):
        ttt = game.initial

        for p in t["pos"]:
            ttt = game.result(ttt, p)
        player = game.to_move(ttt)
        descending = player == 'X'
        sort = sortState_1(ttt, game, player, descending)

        print("=== Test ", i, " ===")
        if descending:
            print("Résultat attendu : états triés par ordre décroissant en fonction de leur évaluation")
        else:
            print("Résultat attendu : états triés par ordre croissant en fonction de leur évaluation")
        game.display(ttt)
        print("Joueur : ", player)

        for i in range(1, len(sort)):
            feval1 = evalState(game.result(ttt, sort[i - 1]), player)
            feval2 = evalState(game.result(ttt, sort[i]), player)

            print("Obtenu : eval( état ", (i - 1), ") = ", feval1, end="")
            if descending:
                print(" >= eval( état ", i, ") = ", feval2, " -> ", end="")

                if feval1 >= feval2:
                    print("OK !")
                else:
                    print("Non OK !")
            else:
                print(" <= eval( état ", i, ") = ", feval2, " -> ", end="")

                if feval1 <= feval2:
                    print("OK !")
                else:
                    print("Non OK !")
        print()

# ______________________________________________________________________________
# V – Etendre le jeu à un damier plus grand.

# ______________________________________________________________________________
# Q1/ Tests de la fonction fEval_2()
def tests_fEval_2():
    testCases = [
        {
            "w": 3,
            "h": 3,
            "k": 3,
            "pos": [(1,1)],
            "expectedX": 0.03
        },
        {
            "w": 5,
            "h": 5,
            "k": 3,
            "pos": [(1,1), (2,2), (1,2), (2,3), (2,1), (3,2)],
            "expectedX": -2.08
        },
        {
            "w": 5,
            "h": 5,
            "k": 4,
            "pos": [(3,3), (2,3), (2,2), (3,2), (2,4), (4,3), (4,4), (3,4), (4,2)],
            "expectedX": 3.96
        },
        {
            "w": 5,
            "h": 5,
            "k": 4,
            "pos": [(1,1), (1,2), (5,1)],
            "expectedX": 0.002
        },
        {
            "w": 10,
            "h": 5,
            "k": 5,
            "pos": [(1,1), (5,1), (1,10), (5,10)],
            "expectedX": 0
        },
        {
            "w": 5,
            "h": 10,
            "k": 5,
            "pos": [(1,1), (10,1), (1,5), (10,5)],
            "expectedX": 0
        }
    ]

    for i,t in enumerate(testCases):
        game = TicTacToe(t["h"], t["w"], t["k"])
        ttt = game.initial

        for p in t["pos"]:
            ttt = game.result(ttt, p)

        print("=== Test ", i, " ===")
        print("Nombre lignes : ", t["h"])
        print("Nombre colonnes : ", t["w"])
        print("Nombre jetons alignés pour gagner : ", t["k"])
        game.display(ttt)

        for p in "XO":
            expected = t["expectedX"]
            if p == 'O':
                expected = -expected

            feval = fEval_2(ttt, p, game)
            print("Résultat attendu pour ", p, " : ", expected, " | Obtenu : ", feval, " -> ", end="")

            if feval == expected:
                print("OK !")
            else:
                print("Non OK !")
        print()

# ______________________________________________________________________________
# Q1/ Tests de la fonction sortState_2()
def tests_sortState_2():
    def evalState(s, p, game):
        if game.terminal_test(s):
            return game.utility(s, p)

        return fEval_2(s, p, game)

    testCases = [
        {
            "w": 3,
            "h": 3,
            "k": 3,
            "pos": []
        },
        {
            "w": 5,
            "h": 5,
            "k": 3,
            "pos": [(1,1), (2,2), (1,2), (2,3), (2,1), (3,2)]
        },
        {
            "w": 5,
            "h": 5,
            "k": 4,
            "pos": [(3,3), (2,3), (2,2), (3,2), (2,4), (4,3), (4,4), (3,4), (4,2)]
        },
        {
            "w": 5,
            "h": 5,
            "k": 4,
            "pos": [(1,1), (1,2), (5,1)]
        },
        {
            "w": 10,
            "h": 5,
            "k": 5,
            "pos": [(1,1), (5,1), (1,10), (5,10)]
        },
        {
            "w": 5,
            "h": 10,
            "k": 5,
            "pos": [(1,1), (10,1), (1,5), (10,5)]
        }
    ]

    for i,t in enumerate(testCases):
        game = TicTacToe(t["h"], t["w"], t["k"])
        ttt = game.initial

        for p in t["pos"]:
            ttt = game.result(ttt, p)
        player = game.to_move(ttt)
        descending = player == 'X'
        sort = sortState_2(ttt, game, player, descending)

        print("=== Test ", i, " ===")
        print("Nombre lignes : ", t["h"])
        print("Nombre colonnes : ", t["w"])
        print("Nombre jetons alignés pour gagner : ", t["k"])
        if descending:
            print("Résultat attendu : états triés par ordre décroissant en fonction de leur évaluation")
        else:
            print("Résultat attendu : états triés par ordre croissant en fonction de leur évaluation")
        game.display(ttt)
        print("Joueur : ", player)

        for i in range(1, len(sort)):
            feval1 = evalState(game.result(ttt, sort[i - 1]), player, game)
            feval2 = evalState(game.result(ttt, sort[i]), player, game)

            print("Obtenu : eval( état ", (i - 1), ") = ", feval1, end="")
            if descending:
                print(" >= eval( état ", i, ") = ", feval2, " -> ", end="")

                if feval1 >= feval2:
                    print("OK !")
                else:
                    print("Non OK !")
            else:
                print(" <= eval( état ", i, ") = ", feval2, " -> ", end="")

                if feval1 <= feval2:
                    print("OK !")
                else:
                    print("Non OK !")
        print()

# ______________________________________________________________________________
# Minimax Search

def minimax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""
    global expandedNodes
    
    player = game.to_move(state)
    prof = 0
    profMax=20
    expandedNodes = 0

    # III. Q1/ Fonction fEval
    def fEval(state):
        # fEval_1() ou fEval_2()
        return fEval_2(state, player, game)

    def max_value(state, prof, profMax):
        global expandedNodes
        prof+=1
        expandedNodes += 1

        if game.terminal_test(state):
            #print "profondeur atteinte {}".format(prof)
            return game.utility(state, player)
        if profMax-prof <= 0:
            return fEval(state)    
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), prof, profMax))
        return v

    def min_value(state, prof, profMax):
        global expandedNodes
        prof+=1
        expandedNodes += 1

        if game.terminal_test(state):
           # print "profondeur atteinte {}".format(prof)
            return game.utility(state, player)
        if profMax-prof <= 0:
            return fEval(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), prof, profMax))
        return v

    # Body of minimax_decision:
    return argmax(game.actions(state),
                  key=lambda a: min_value(game.result(state, a), prof, profMax))

# ______________________________________________________________________________

def alphabeta_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""
    global expandedNodes
    
    player = game.to_move(state)
    prof = 0
    profMax=20
    expandedNodes = 0

    # III. Q1/ Fonction fEval
    def fEval(state):
        # fEval_1() ou fEval_2()
        return fEval_2(state, player, game)

    # IV. Q1/ Ordonnancement des noeuds
    def sortState(state, descending):
        # sortState_1() qui utilise fEval_1()
        # ou sortState_2() qui utilise fEval_2()
        return sortState_2(state, game, player, descending)
    
    # Functions used by alphabeta
    def max_value(state, prof, alpha, beta):
        global expandedNodes
        prof+=1
        expandedNodes += 1
        if game.terminal_test(state):
            return game.utility(state, player)
        if profMax-prof <= 0:
            return fEval(state)
        v = -infinity
        for a in sortState(state, True): # IV. Q1/ Ordonnancement des noeuds
            v = max(v, min_value(game.result(state, a), prof, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, prof, alpha, beta):
        global expandedNodes
        prof+=1
        expandedNodes += 1    
        if game.terminal_test(state):
            return game.utility(state, player)
        if profMax-prof <= 0:
            return fEval(state)       
        v = infinity
        for a in sortState(state, False): # IV. Q1/ Ordonnancement des noeuds
            v = min(v, max_value(game.result(state, a), prof, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search:
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in sortState(state, True): # IV. Q1/ Ordonnancement des noeuds
        v = min_value(game.result(state, a), prof, best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

def alphabeta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

# ______________________________________________________________________________
# Players for Games

def query_player(game, state):
    """Make a move by querying standard input."""
    print("current state:")
    game.display(state)
    print("available moves: {}".format(game.actions(state)))
    print("")
    move_string = input('Your move? ')
    try:
        move = eval(move_string)
    except NameError:
        move = move_string
    return move


def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state))


def alphabeta_player(game, state):
    res =  alphabeta_search(state, game)
    return res

def minimax_player(game, state):
    res =  minimax_decision(state, game)
    print("noeuds developpes : " +str(expandedNodes))
    return res
# ______________________________________________________________________________
# Some Sample Games


class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


class Fig52Game(Game):
    """The game represented in [Figure 5.2]. Serves as a simple test case."""

    succs = dict(A=dict(a1='B', a2='C', a3='D'),
                 B=dict(b1='B1', b2='B2', b3='B3'),
                 C=dict(c1='C1', c2='C2', c3='C3'),
                 D=dict(d1='D1', d2='D2', d3='D3'))
    utils = dict(B1=3, B2=12, B3=8, C1=2, C2=4, C3=6, D1=14, D2=5, D3=2)
    initial = 'A'

    def actions(self, state):
        return list(self.succs.get(state, {}).keys())

    def result(self, state, move):
        return self.succs[state][move]

    def utility(self, state, player):
        if player == 'MAX':
            return self.utils[state]
        else:
            return -self.utils[state]

    def terminal_test(self, state):
        return state not in ('A', 'B', 'C', 'D')

    def to_move(self, state):
        return 'MIN' if state in 'BCD' else 'MAX'


class Fig52Extended(Game):
    """Similar to Fig52Game but bigger. Useful for visualisation"""

    succs = {i:dict(l=i*3+1, m=i*3+2, r=i*3+3) for i in range(13)}
    utils = dict()

    def actions(self, state):
        return sorted(list(self.succs.get(state, {}).keys()))

    def result(self, state, move):
        return self.succs[state][move]

    def utility(self, state, player):
        if player == 'MAX':
            return self.utils[state]
        else:
            return -self.utils[state]

    def terminal_test(self, state):
        return state not in range(13)

    def to_move(self, state):
        return 'MIN' if state in {1, 2, 3} else 'MAX'

class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 10 for win, -10 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 10; if 'O' wins return -10; else return 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +10 if player == 'X' else -10
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k


class ConnectFour(TicTacToe):
    """A TicTacToe-like game in which you can only make a move on the bottom
    row, or in a square directly above an occupied square.  Traditionally
    played on a 7x6 board and requiring 4 in a row."""

    def __init__(self, h=7, v=6, k=4):
        TicTacToe.__init__(self, h, v, k)

    def actions(self, state):
        return [(x, y) for (x, y) in state.moves
                if y == 1 or (x, y - 1) in state.board]

from reponses import *
from tests_reponses import *