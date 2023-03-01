/* Louka DOZ */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <limits.h>

/* Taille lignes/colonnes */
#define ROW_COL_SIZE 3
/* Taille plateau */
#define BOARD_SIZE 9
/* Nombre de movements possibles (Nord, Sud, Est, Ouest) */
#define MOVE_COUNT 4
/* Nombre d'algorithmes */
#define NUMBER_OF_ALGORITHMS 5
/* Nombre d'heuristique */
#define NUMBER_OF_HEURISTICS 3

/* Numéros algortithmes */
#define BF 0
#define DF 1
#define DL 2
#define ID 3
#define AA 4

/******************* Exercice 1 *******************/
/* Plateau */
typedef struct board {
  int board [BOARD_SIZE];
} board;

/* Mouvement possibles du trou */
typedef enum move {
  WEST,
  EAST,
  SOUTH,
  NORTH
  
} move;

/* Afficher un plateau */
void display_board(board* b) {
  for(int j = 0; j < ROW_COL_SIZE; j++) {
    for(int i = 0; i < ROW_COL_SIZE; i++) {
      printf("+---");
    }

    printf("+\n");
    for(int i = 0; i < ROW_COL_SIZE; i++) {
      if(b->board[i + ROW_COL_SIZE * j] == 0)
        printf("|   ");
      else
        printf("| %d ", b->board[i + ROW_COL_SIZE * j]);
    }

    printf("|\n");
  }

  for(int i = 0; i < ROW_COL_SIZE;i ++) {
    printf("+---");
  }

  printf("+\n");
}

/* Echanger les valeurs d'un plateau */
void switch_val(board* b, int x1, int x2) {
  int tmp = b->board[x1];

  b->board[x1] = b->board[x2];
  b->board[x2] = tmp;
}

/* Obtenir la position du trou d'un plateau */
int get_hole_pos(board* b) {
  for(int i = 0; i < BOARD_SIZE; i++) {
    if(b->board[i] == 0)
      return i;
  }

  return -1;
}

/* Copier un plateau */
board* copy_board(board* b) {
  board* new_b = (board*) malloc(sizeof(board));

  for(int i = 0; i < BOARD_SIZE; i++)
    new_b->board[i] = b->board[i];

  return new_b;
}

/* Déplacer le trou */
board* move_board(board* b, move m) {
  int hole_pos = get_hole_pos(b);
  board* new_b = NULL;

  switch(m) {
    case NORTH:
      if(hole_pos >= ROW_COL_SIZE) {
        new_b = copy_board(b);
        switch_val(new_b, hole_pos, hole_pos - ROW_COL_SIZE);
      }

      break;

    case SOUTH:
      if(hole_pos < BOARD_SIZE - ROW_COL_SIZE) {
        new_b = copy_board(b);
        switch_val(new_b, hole_pos, hole_pos + ROW_COL_SIZE);
      }

      break;

    case WEST:
      if(hole_pos % ROW_COL_SIZE != 0) {
        new_b = copy_board(b);
        switch_val(new_b, hole_pos, hole_pos - 1);
      }

      break;

    case EAST:
      if(hole_pos % ROW_COL_SIZE != ROW_COL_SIZE - 1) {
        new_b = copy_board(b);
        switch_val(new_b, hole_pos, hole_pos + 1);
      }

      break;
  }

  return new_b;
}

/* Le plateau est final */
int is_final(board* b) {
  for(int i = 0; i < BOARD_SIZE; i++) {
    if(b->board[i] != i)
      return 0;
  }

  return 1;
}

/* Initialiser un plateau */
board* init_board(int* start_board, int nb_random_moves) {
  board* b = (board*) malloc(sizeof(board));

  for(int i = 0; i < BOARD_SIZE; i++)
    b->board[i] = start_board[i];

  for(int i = 0; i < nb_random_moves; i++) {
    board* new_b = move_board(b, rand() % MOVE_COUNT);

    if(new_b != NULL) {
      free(b);
      b = new_b;
    }
  }

  return b;
}

/******************* Exercice 2 *******************/
typedef struct node node;

/* Noeud */
struct node {
  board* board;
  node* next;
  int depth;
  int cost; /* Exercice 3 */
};

/* Nouveau noeud */
node* new_node(board* b, int depth) {
  node* n = (node*) malloc(sizeof(node));

  n->board = b;
  n->next = NULL;
  n->depth = depth;
  n->cost = 0;

  return n;
}

/* Ajouter noeud à une file */
void push_queue(node** first, node* new) {
  if(*first == NULL)
    *first = new;
  else {
    node* n = *first;

    while(n->next != NULL)
      n = n->next;

    n->next = new;
  }
}

/* Ajouter noeud à une pile */
void push_heap(node** first, node* new) {
  if(*first == NULL)
    *first = new;
  else {
    new->next = *first;
    *first = new;
  }
}

/* Ajouter noeud à la file des noeud traités */
void push_treated(node** first, node* new) {
  if(*first == NULL)
    *first = new;
  else {
    node* before = NULL;
    node* after = *first;

    /* Trier selon la profondeur par ordre décroissant */
    while(after->next != NULL && after->depth > new->depth) {
      before = after;
      after = after->next;
    }

    if(before == NULL) {
      new->next = after;
      *first = new;
    } else {
      new->next = after;
      before->next = new;
    }
  }
}

/* Debugger des noeuds */
void debug_nodes(node* first) {
  node* n = first;

  printf("DEBUG NODES : {\n");
  while(n != NULL) {
    display_board(n->board);
    printf("DEPTH : %d\n", n->depth);
    printf("COST : %d\n", n->cost);

    n = n->next;
  }

  printf("}\n");
}

/* Retirer le premier noeud d'une liste ou pile */
node* pop(node** first) {
  node* n = *first;

  *first = n->next;

  return n;
}

/* Est-ce qu'un plateau est présent dans une liste ou pile */
int contains_board(node* first, board* b) {
  if(first == NULL)
    return 0;

  node* n = first;
  int exists;

  while(n != NULL) {
    exists = 1;

    for(int i = 0; i < BOARD_SIZE; i++) {
      if(b->board[i] != n->board->board[i]){
        exists = 0;
        break;
      }
    }

    if(exists)
      return 1;

    n = n->next;
  }

  return 0;
}

/* Est-ce qu'un plateau est présent dans une pile pour la Recherche en profondeur limitée
  -> Permettre de traiter des noeuds déjà fais mais d'une profondeur plus petite */
int contains_board_limited_deepening_search(node* first, board* b, int depth) {
  if(first == NULL)
    return 0;

  node* n = first;
  int exists;

  while(n != NULL) {
    /* Considérer que les mêmes configurations mais d'une profondeur plus petite comme non traitées */
    if(depth >= n->depth) {
      exists = 1;

      for(int i = 0; i < BOARD_SIZE; i++) {
        if(b->board[i] != n->board->board[i]){
          exists = 0;
          break;
        }
      }

      if(exists)
        return 1;
    }

    n = n->next;
  }

  return 0;
}

/* Est-ce qu'une profondeur est présente dans une liste ou pile
D'où l'intérêt de trier par profondeur */
int contains_depth(node* first, int depth) {
  if(first == NULL)
    return 0;

  node* n = first;

  while(n != NULL && n->depth > depth)
    n = n->next;

  if(n->depth == depth)
    return 1;

  return 0;
}

/* Free noeud */
void free_nodes(node* first) {
  node* n = first;

  while(n != NULL) {
    node* next = n->next;
    free(n->board);
    free(n);

    n = next;
  }
}

/* Recherche en largeur d’abord */
int breadth_first_search(board* start, int show_new_depth, int* treated_nodes_count, int* plays_count) {
  node* queue = new_node(start, 0);
  node* treated = NULL;
  int final = -1;

  while(queue != NULL) {
    node* n = pop(&queue);
    board* b = n->board;

    if(!contains_board(treated, b)) {
      (*treated_nodes_count)++;

      if(show_new_depth && !contains_depth(treated, n->depth))
        printf("Nouvelle profondeur atteinte : %d\n", n->depth);

      if(is_final(b)) {
        final = n->depth;
        *plays_count = n->depth;
        break;
      }

      for(int i = 0; i < MOVE_COUNT; i++) {
        board* mv = move_board(b, i);

        if(mv != NULL)
          push_queue(&queue, new_node(mv, n->depth + 1));
      }

      push_treated(&treated, n);
    }
  }

  free_nodes(queue);
  free_nodes(treated);
  return final;
}

/* Recherche en profondeur d’abord */
int depth_first_search(board* start, int show_new_depth, int* treated_nodes_count, int* plays_count) {
  node* heap = new_node(start, 0);
  node* treated = NULL;
  int final = -1;

  while(heap != NULL) {
    node* n = pop(&heap);
    board* b = n->board;

    if(!contains_board(treated, b)) {
      (*treated_nodes_count)++;

      if(show_new_depth && !contains_depth(treated, n->depth))
        printf("Nouvelle profondeur atteinte : %d\n", n->depth);

      if(is_final(b)) {
        final = n->depth;
        *plays_count = n->depth;
        break;
      }

      for(int i = 0; i < MOVE_COUNT; i++) {
        board* mv = move_board(b, i);

        if(mv != NULL)
          push_heap(&heap, new_node(mv, n->depth + 1));
      }

      push_treated(&treated, n);
    }
  }

  free_nodes(heap);
  free_nodes(treated);
  return final;
}

/* Recherche en profondeur limitée */
int depth_limited_search(board* start, int max_depth, int show_new_depth, int* treated_nodes_count, int* plays_count) {
  node* heap = new_node(start, 0);
  node* treated = NULL;
  int final = -1;

  while(heap != NULL) {
    node* n = pop(&heap);
    board* b = n->board;

    if(!contains_board_limited_deepening_search(treated, b, n->depth)) {
      (*treated_nodes_count)++;
      
      if(show_new_depth && !contains_depth(treated, n->depth))
        printf("Nouvelle profondeur atteinte : %d\n", n->depth);

      if(is_final(b)) {
        final = n->depth;
        *plays_count = n->depth;
        break;
      }

      if(n->depth < max_depth) {
        for(int i = 0; i < MOVE_COUNT; i++) {
          board* mv = move_board(b, i);

          if(mv != NULL)
            push_heap(&heap, new_node(mv, n->depth + 1));
        }
      }

      push_treated(&treated, n);
    }
  }

  free_nodes(heap);
  free_nodes(treated);
  return final;
}

/* Recherche en profondeur itérative */
int iterative_deepening_search(board* start, int show_new_depth, int* treated_nodes_count, int* plays_count) {
  int i = 1;
  int final = -1;
  int treated_nodes_total = 0;

  while(1) {
    *treated_nodes_count = 0;

    printf("\n========== Iterative deepening search (max depth = %d) ==========\n", i);
    final = depth_limited_search(copy_board(start), i, show_new_depth, treated_nodes_count, plays_count);
    treated_nodes_total += *treated_nodes_count;
    printf("Treated nodes : %d\n", *treated_nodes_count);

    if(final >= 0)
      break;

    i++;
  }

  *treated_nodes_count = treated_nodes_total;
  free(start);
  return final;
}

/******************* Exercice 3 *******************/
/* Obtenir la ligne d'une position */
int get_row(int pos) {
  int row = 0;

  for(; pos >= ROW_COL_SIZE; pos -= ROW_COL_SIZE) {
    row++;
  }

  return row;
}

/* Obtenir la colonne d'une position */
int get_column(int pos) {
  return pos % 3;
}

/* Heuristique 1 */
int h1(board* b) {
  int count = 0;

  for(int i = 0; i < BOARD_SIZE; i++) {
    if(b->board[i] != i)
      count++;
  }

  return count;
}

/* Heuristique 2 */
int h2(board* b) {
  int count = 0;

  for(int i = 0; i < BOARD_SIZE; i++) {
    int pos = 0;

    for(int j = 0; j < BOARD_SIZE; j++) {
      if(b->board[j] == i) {
        pos = j;
        break;
      }
    }

    int row_distance = get_row(i) - get_row(pos);
    int column_distance = get_column(i) - get_column(pos);

    if(row_distance < 0)
      row_distance = row_distance * -1;

    if(column_distance < 0)
      column_distance = column_distance * -1;

    count += row_distance + column_distance;
  }

  return count;
}

/* Obtenir la valeur précédente dans le plateau d'une valeur donnée */
int get_previous(int i) {
  int row = get_row(i);
  int column = get_column(i);
  int previous;

  if(row == 0) {
    if(column > 0)
      previous = i - 1;
    else
      previous = i + ROW_COL_SIZE;

  } else if(row == ROW_COL_SIZE - 1) {
    if(column < ROW_COL_SIZE - 1)
      previous = i + 1;
    else
      previous = i - ROW_COL_SIZE;

  } else
    previous = i - ROW_COL_SIZE;

  return previous;
}

/* Obtenir la valeur suivante dans le plateau d'une valeur donnée */
int get_next(int i) {
  int row = get_row(i);
  int column = get_column(i);
  int next;

  if(row == 0) {
    if(column < ROW_COL_SIZE - 1)
      next = i + 1;
    else
      next = i + ROW_COL_SIZE;

  } else if(row == ROW_COL_SIZE - 1) {
    if(column > 0)
      next = i - 1;
    else
      next = i - ROW_COL_SIZE;

  } else 
    next = i + ROW_COL_SIZE;

  return next;
}

/* Heuristique 3 */
int h3(board* b) {
  int count = h2(b);
  int half = BOARD_SIZE / 2;

  for(int i = 0; i < BOARD_SIZE; i++) {
    int score = 0;

    if(i == half && b->board[i] != half)
      score = 1;
    else {
      int previous_pos = get_previous(i);
      int next_pos = get_next(i);
      int previous_val = get_previous(b->board[i]);
      int next_val = get_next(b->board[i]);

      if(previous_pos != previous_val)
        score++;

      if(next_pos != next_val)
        score++;
    }

    count += ROW_COL_SIZE * score;
  }

  return count;
}

/* Heuristique */
typedef int (*heuristic)(board*);

/* Liste de priorité de noeuds */
node* new_priority_node(board* b, int depth, int cost) {
  node* n = (node*) malloc(sizeof(node));

  n->board = b;
  n->next = NULL;
  n->depth = depth;
  n->cost = cost;

  return n;
}

/* Ajouter un noeud dans une file de priorité */
void push_priority(node** first, node* new) {
  if(*first == NULL)
    *first = new;
  else if(new->cost <= (*first)->cost) {
    new->next = *first;
    *first = new;
  } else {
    node* before = NULL;
    node* after = *first;

    /* Trier par coût dans l'ordre décroissant */
    while(after != NULL && new->cost > after->cost) {
      before = after;
      after = after->next;
    }

    if(before == NULL) {
      after->next = new;
    } else {
      new->next = after;
      before->next = new;
    }
  }
}

/* Est-ce qu'un noeud est contenu dans une file de priorité */
int contains_priority(node* first, board* b, int cost) {
  if(first == NULL)
    return 0;

  node* n = first;
  int exists;

  while(n != NULL) {
    /* Considérer que les mêmes configurations mais avec un score plus petit comme non traitées */
    if(cost >= n->cost) {
      exists = 1;

      for(int i = 0; i < BOARD_SIZE; i++) {
        if(b->board[i] != n->board->board[i]){
          exists = 0;
          break;
        }
      }

      if(exists)
        return 1;
    }

    n = n->next;
  }

  return 0;
}

/* Algorithme A* */
int algorithm_A(board* start, heuristic h, int show_new_depth, int* treated_nodes_count, int* plays_count) {
  node* priority = new_node(start, 0);
  node* treated = NULL;
  int final = -1;

  while(priority != NULL) {
    node* n = pop(&priority);
    board* b = n->board;

    if(!contains_priority(treated, b, n->cost)) {
      (*treated_nodes_count)++;
      
      if(show_new_depth && !contains_depth(treated, n->depth))
        printf("Nouvelle profondeur atteinte : %d\n", n->depth);

      if(is_final(b)) {
        final = n->depth;
        *plays_count = n->depth;
        break;
      }

      for(int i = 0; i < MOVE_COUNT; i++) {
        board* mv = move_board(b, i);

        if(mv != NULL)
          push_priority(&priority, new_priority_node(mv, n->depth + 1, n->depth + 1 + h(mv)));
      }

      push_treated(&treated, n);
    }
  }

  free_nodes(priority);
  if(treated != NULL)
    free_nodes(treated);
  return final;
}

/* Afficher le résultat d'un algorithme */
void printResult(int final, int treated_nodes_count, int plays_count, clock_t start_time) {
  if(final >= 0) { 
    printf("\nConfiguration final trouvée à la profondeur : %d\n", final);
    printf("Nombres de couts pour atteindre la configuration finale : %d\n", plays_count);
  } else
    printf("\nConfiguration finale non trouvée\n");

  printf("Noeuds traités : %d\n", treated_nodes_count);
  printf("Temps : %f secondes\n", (float) (clock() - start_time) / CLOCKS_PER_SEC);
}

/* Afficher l'usage */
void printUsage() {
  printf("Usage : exec [-r <number of random moves>] [-d <max depth>] [-b <start board>] [-i] [-bf] [-df] [-dl] [-id] [-a]\n");
  printf("-r <number of random moves> : Nombre de mouvements pour initialiser un plateau (defaut : 100, min : 0, max : INT_MAX)\n");
  printf("-d <max depth> : Profondeur max pour l'algorithme de Recherche en profondeur d'abord (defaut : 20, min : 0, max : INT_MAX)\n");
  printf("-b <start board> : Plateau de départ (defaut : 012345678)\n");
  printf("-i : Afficher une ligne dès qu'une nouvelle profondeur est atteinte (défaut : non)\n");
  printf("-bf : Algorithme de Recherche en largeur d'abord\n");
  printf("-df : Algorithme de Recherche en profondeur d'abord\n");
  printf("-dl : Algorithme de Recherche en profondeur limitée\n");
  printf("-id : Algorithme de Recherche en profondeur itérative\n");
  printf("-a : Algorithme A*\n");
  printf("Tous les algorithmes seront lancés si aucun argument ne précise les algorithmes à lancer\n");
}

/* Vérifier qu'un argument int est correct */
int checkArgValue(char* arg, int min, int max, int* ret) {
  char* end;
  int val = strtol(arg, &end, 10);

  if(arg != end && val >= min && val <= max) {
    *ret = val;

    return 1;
  }

  return 0;
}

/* 
  Usage : exec [-r <number of random moves>] [-d <max depth>] [-b <start board>] [-i] [-bf] [-df] [-dl] [-id] [-a]
  -r <number of random moves> : Nombre de mouvements pour initialiser un plateau (defaut : 100, min : 0, max : INT_MAX)
  -d <max depth> : Profondeur max pour l'algorithme de Recherche en profondeur d'abord (defaut : 20, min : 0, max : INT_MAX)
  -b <start board> : Plateau de départ (defaut : 012345678)
  -i : Afficher une ligne dès qu'une nouvelle profondeur est atteinte (défaut : non)
  -bf : Algorithme de Recherche en largeur d'abord
  -df : Algorithme de Recherche en profondeur d'abord
  -dl : Algorithme de Recherche en profondeur limitée
  -id : Algorithme de Recherche en profondeur itérative
  -a : Algorithme A*
  Tous les algorithmes seront lancés si aucun argument ne précise les algorithmes à lancer
*/
int main(int argc, char* argv[]) {
  int nb_random_moves = 100;
  int max_depth = 20;
  int i_val = 0;
  int algorithms[NUMBER_OF_ALGORITHMS] = {0, 0, 0, 0, 0};
  int start_board[BOARD_SIZE] = {0, 1, 2, 3, 4, 5, 6, 7, 8};

  srand(time(NULL));

  if(argc > 1) {
    for(int i = 1; i < argc; i++) {
      /* Profondeur max pour l'algorithme de Recherche en profondeur limitée */
      if(strcmp(argv[i], "-d") == 0) {
        if(argc > i + 1) {
          if(!checkArgValue(argv[i + 1], 0, INT_MAX, &max_depth)) {
            printf("Argument invalide : %s\n", argv[i + 1]);
            printUsage();

            return EXIT_FAILURE;
          }

          i++;
        } else {
          printf("Pas assez d'arguments\n");
          printUsage();

          return EXIT_FAILURE;
        }
      /* Nombre de mouvements aléatoires pour initialiser un plateau */
      } else if(strcmp(argv[i], "-r") == 0) {
        if(argc > i + 1) {
          if(!checkArgValue(argv[i + 1], 0, INT_MAX, &nb_random_moves)) {
            printf("Argument invalide : %s\n", argv[i + 1]);
            printUsage();

            return EXIT_FAILURE;
          }

          i++;
        } else {
          printf("Pas assez d'arguments\n");
          printUsage();

          return EXIT_FAILURE;
        }
      /* Plateau de départ */
      } else if(strcmp(argv[i], "-b") == 0) {
        if(argc > i + 1) {
          char c[2];
          char* board = argv[i + 1];
          int len = strlen(board);
          int b_val = 0;

          if(len == BOARD_SIZE) {
            for(int i = 0; i < len; i++) {
              sprintf(c, "%c", board[i]);

              for(int j = 0; j < len; j++) {
                if(i != j && board[i] == board[j]) {
                  printf("Argument invalide : %s\n", board);
                  printUsage();

                  return EXIT_FAILURE;
                }
              }

              if(checkArgValue(c, 0, BOARD_SIZE - 1, &b_val))
                start_board[i] = b_val;
              else {
                printf("Argument invalide : %s\n", board);
                printUsage();

                return EXIT_FAILURE;
              }
            }

            i++;
          } else {
            printf("Argument invalide : %s\n", argv[i + 1]);
            printUsage();

            return EXIT_FAILURE;
          }
        } else {
          printf("Pas assez d'arguments\n");
          printUsage();

          return EXIT_FAILURE;
        }
      /* Afficher les nouvelles profondeurs */
      } else if(strcmp(argv[i], "-i") == 0) {
         i_val = 1;
      /* Algorithme de Recherche en largeur d'abord */
      } else if(strcmp(argv[i], "-bf") == 0) {
          algorithms[BF] = 1;
      /* Algorithme de Recherche en profondeur d'abord */
      } else if(strcmp(argv[i], "-df") == 0) {
          algorithms[DF] = 1;
      /* Algorithme de Recherche en profondeur limitée */
      } else if(strcmp(argv[i], "-dl") == 0) {
          algorithms[DL] = 1;
      /* Algorithme de Recherche en profondeur itérative */
      } else if(strcmp(argv[i], "-id") == 0) {
          algorithms[ID] = 1;
      /* Algorithme A* */
      } else if(strcmp(argv[i], "-a") == 0) {
          algorithms[AA] = 1;
      /* Algorithme inconnu */
      } else {
        printf("Argument inconnu : %s\n", argv[i]);
        printUsage();

        return EXIT_FAILURE;
      }
    }
  }

  /* Initialisation */
  board* b = init_board(start_board, nb_random_moves);
  int treated_nodes_count = 0;
  int plays_count = 0;
  int final = -1;
  int algo_arg = 1;
  clock_t start_time;

  /* Vérifier si un argument concerne un algorithme */
  for(int i = 0; i < NUMBER_OF_ALGORITHMS; i++) {
    if(algorithms[i]) {
      algo_arg = 0;
      break;
    }
  }

  /* Lancer tous les algorithmes si aucun algorithme précis n'a été demandé en argument */
  if(algo_arg) {
    for(int i = 0; i < NUMBER_OF_ALGORITHMS; i++) {
      algorithms[i] = 1;
    }
  }

  printf("========== Configuration de départ (%d mouvements aléatoires) ==========\n", nb_random_moves);
  display_board(b);

  /* Algorithme de Recherche en largeur d'abord */
  if(algorithms[BF]) {
    printf("\n========== Recherche en largeur d'abord ==========\n");
    treated_nodes_count = 0;
    plays_count = 0;
    start_time = clock();

    final = breadth_first_search(copy_board(b), i_val, &treated_nodes_count, &plays_count);
    printResult(final, treated_nodes_count, plays_count, start_time);
  }

  /* Algorithme de Recherche en profondeur d'abord */
  if(algorithms[DF]) {
    printf("\n========== Recherche en profondeur d'abord ==========\n");
    treated_nodes_count = 0;
    plays_count = 0;
    start_time = clock();

    final = depth_first_search(copy_board(b), i_val, &treated_nodes_count, &plays_count);
    printResult(final, treated_nodes_count, plays_count, start_time);
  }

  /* Algorithme de Recherche en profondeur limitée */
  if(algorithms[DL]) {
    printf("\n========== Recherche en profondeur limitée (profondeur max = %d) ==========\n", max_depth);
    treated_nodes_count = 0;
    plays_count = 0;
    start_time = clock();

    final = depth_limited_search(copy_board(b), max_depth, i_val, &treated_nodes_count, &plays_count);
    printResult(final, treated_nodes_count, plays_count, start_time);
  }

  /* Algorithme de Recherche en profondeur itérative */
  if(algorithms[ID]) {
    printf("\n========== Recherche en profondeur itérative ==========\n");
    treated_nodes_count = 0;
    plays_count = 0;
    start_time = clock();

    final = iterative_deepening_search(copy_board(b), i_val, &treated_nodes_count, &plays_count);
    printResult(final, treated_nodes_count, plays_count, start_time);
  }

  /* Algorithme A* */
  if(algorithms[AA]) {
    heuristic h[NUMBER_OF_HEURISTICS] = {&h1, &h2, &h3};

    for(int i = 0; i < NUMBER_OF_HEURISTICS; i++) {
      printf("\n========== algorithme A* (heuristique = h%d) ==========\n", i + 1);
      treated_nodes_count = 0;
      plays_count = 0;
      start_time = clock();

      final = algorithm_A(copy_board(b), h[i], i_val, &treated_nodes_count, &plays_count);
      printResult(final, treated_nodes_count, plays_count, start_time);
    }
  }

  free(b);

  return EXIT_SUCCESS;
}