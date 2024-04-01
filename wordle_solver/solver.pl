elt(X, [X | _]) :- !.
elt(X, [_ | L]) :- elt(X, L).

% Exercice 1

% Question 1
availables([], _, []).
availables([X | P], [Y | S], A) :- X = Y, availables(P, S, A).
availables([X | P], [Y | S], [Y | A]) :- X \= Y, availables(P, S, A).

% Question 2
mem_remove(_, [], []).
mem_remove(X, [Y | L], L) :- X == Y, !.
mem_remove(X, [Y | L], [Y | Q]) :- X \= Y, mem_remove(X, L, Q).

% Question 3
color_with_availables([], _, _, []).
color_with_availables([X | P], [Y | S], A, [green | C]) :- X == Y, color_with_availables(P, S, A, C).
color_with_availables([X | P], [Y | S], A, [orange | C]) :- X \= Y, elt(X, A), mem_remove(X, A, B), color_with_availables(P, S, B, C).
color_with_availables([X | P], [Y | S], A, [black | C]) :- X \= Y, \+ elt(X, A), color_with_availables(P, S, A, C).

% Question 4
color(P, S, C) :- availables(P, S, A), color_with_availables(P, S, A, C).

% Exercice 2

% Question 5
check_colors([], [], []).
check_colors([X | P], [Y | O], [Z | C]) :- Z == green, X == Y, check_colors(P, O, C).
check_colors([X | P], [Y | O], [Z | C]) :- Z \= green, X \= Y, check_colors(P, O, C).

% Question 6
must_be_present([], [], []).
must_be_present([X | O], [Y | C], [X | A]) :- Y == orange, must_be_present(O, C, A).
must_be_present([_ | O], [Y | C], A) :- Y \= orange, must_be_present(O, C, A).

% Question 7
forbidden([], [], []).
forbidden([X | O], [Y | C], F) :- Y == black, elt(X, F), forbidden(O, C, F).
forbidden([X | O], [Y | C], [X | F]) :- Y == black, forbidden(O, C, F).
forbidden([_ | O], [Y | C], F) :- Y \= black, forbidden(O, C, F).

% Question 8
remove_green([], [], []).
remove_green([X | P], [Y | C], [X | R]) :- Y \= green, remove_green(P, C, R).
remove_green([_ | P], [Y | C], R) :- Y == green, remove_green(P, C, R).

% Question 9
check_presence_and_forbidden([], [], _).
check_presence_and_forbidden([X | P], A, F) :- elt(X, A), mem_remove(X, A, B), check_presence_and_forbidden(P, B, F).
check_presence_and_forbidden([X | P], [], F) :- \+ elt(X, F), check_presence_and_forbidden(P, [], F).
check_presence_and_forbidden([X | P], A, F) :- \+ elt(X, F), \+ elt(X, A), check_presence_and_forbidden(P, A, F).

% Question 10
check_one(P, O, C) :- check_colors(P, O, C), must_be_present(O, C, A), forbidden(O, C, F), remove_green(P, C, R), check_presence_and_forbidden(R, A, F).

% Question 11
check_all(_, [], []).
check_all(P, [O | OS], [C | CS]) :- check_one(P, O, C), !, check_all(P, OS, CS).

% Question 12
:- [sorting/source/best].

suggest(P, OS, CS) :- word(P), check_all(P, OS, CS).

% Question 13
% Il suffit de renseigner OS = liste de propositions et CS = liste de leurs colorations
% mais sans renseigner P dans suggest(P, OS, CS).

% Exercice 3

% Question 14
play_n_steps(_, 0, [], []).
play_n_steps(S, N, [P | PS], [C | CS]) :- N > 0, R is N - 1, play_n_steps(S, R, PS, CS), suggest(P, PS, CS), !, color(P, S, C).

% Question 15
% play(S, []) :- \+ play_n_steps(S, 6, _, _).
play(S, PS) :- play_n_steps(S, 6, PS, _).

% Question 16
success(S) :- word(S), play(S, [P | _]), P == S.

% Question 17
number_of_solutions(N) :- findall(L, success(L), R), length(R, N).

% Question 18
% Initialement, avec le fichier word.pl de base, on obtient 6436 mot trouvés

% 1. Inspiration
% Pour améliorer ce score, je suis allé me documenter auprès d'une vidéo de la chaîne YouTube ScienceEtonnante (https://www.youtube.com/watch?v=iw4_7ioHWF4),
% dont je me suis souvenu l'avoir regardé lors de sa sortie quelques mois auparavant.
% Dans cette vidéo, l'auteur explique s'être inspiré d'un vidéo de la chaine 3Blue1Brown (https://www.youtube.com/watch?v=v68zYyaEmEA&t=0s),
% que j'ai aussi pris la peine de regarder
% Ces vidéo expliquent comment résoudre Wordle grâce à la théorie de l'information. Autrement dit, on cherche a mesurer l'information moyenne que
% l'on peut espérer gagner si l'on choisi tel mot. De même que pour le juste prix, si l'on cherche un nombre entre 1 et 100, en disant 50, on est
% sûr d'au moins retirer la moitié des possibilités. A l'inverse, en disant 10, on prend le risque de ne retirer que 10% des solutions possibles
% mais on peut aussi gagner 90% de solutions possibles en moins.

% 2. Probabilité
% Pour appliquer ce principe aux mots, il faut calculer la probabilité de chaque coloration possible pour chacun des mots (voir possible_colors.txt).
% Pour cela, pour chaque mot M, j'ai généré toutes ses colorations possibles en le comparant a chaque mot S, comme si S était la solution, 
% et j'ai ensuite calculé, parmi tous les mots P, combien de mots P étaient des solution valides pour chaque coloration de tous les mots M.
% La probabilité d'une couleur C d'un mot M est : P(C) = nb mots valides / nb mots total. (Voir probability.txt).
% Par exemple, si je compare M = "abaca" avec une solution S = "abaca", j'obtien la coloration "ggggg". Je regarde combien de mots sont valides
% face à cette coloration et j'obtien P("ggggg") = 1 / 7980, car seul un mot est valide face à cette coloration et c'est "abaca" lui-même.
% On a donc réduit notre nombre de solution total à 1, ce qui est parfait car cela signifie que le mot a été trouvé.

% 3. Bits d'information
% Avec la probabilité, on peut calculer l'information de la coloration C d'un mot : I(C) = log2(1 / P(C)). Cette information, appelée "bits",
% permet de savoir a quel point le nombre de possibilités a été réduit (voir probability.txt). 
% Par exemple, I(C) = 1 bit correspond à un nombre de possiblités divisé par 2. 2 bits c'est divisé par 4. 
% Plus l'information est grande, moins il y a de possibilités restantes, donc plus c'est interressant.

% 4. Information d'un mot
% Pour estimer l'information d'un mot M, il suffit de faire la moyenne des informations apportées par chaque couleur :
% I(M) = SOMME(c) P(c) * log2(1 / P(c)), pour chaque coloration possible c de M
% Il ne reste plus qu'a trier par ordre décroissant en fonction de l'information pour obtenir les mots les plus interressants (voir info.txt).

% 5. Conclusion
% Au final, le fichier word.pl généré par la théorie de l'information que j'ai obtenu permet de trouver avec succès 7220 mots.
% Bien que largement meilleur que 6436, je reste assez déçu de ce chiffre d'autant plus qu'il est loin d'être parfait. En effet, en plaçant
% "tarie" en premier, on peut déjà améliorer le score jusqu'à 7295.
% Ce qui peut expliquer ce chiffre, c'est peut être que la théorie de l'information, telle qu'utilisé dans les vidéo citées précédemment,
% sert a obtenir le meilleur mot à chaque tour, en fonction de ce qui a été joué précédemment. A l'inverse, dans ce TP, les mots sont toujours
% classés pareils pour tous les tours d'une partie.
% De plus, la fréquence d'utilisation des mots (si c'est des mots communs ou plutôt inconnus) n'est pas non plus prise en compte.