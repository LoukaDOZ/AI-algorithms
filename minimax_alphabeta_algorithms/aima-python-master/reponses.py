from games import *

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