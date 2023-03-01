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