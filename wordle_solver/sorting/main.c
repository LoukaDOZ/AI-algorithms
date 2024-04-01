#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <sys/time.h>

#define WORD_LEN 5
#define NB_PATTERNS 243
#define PROGRESS_BAR_SIZE 10
#define DEFAULT_SOURCE_FILE "./source/words_origin.pl"
#define DEFAULT_DEST_FOLDER "./result/"
#define WORDS_DEST_FILE "words.pl"
#define INFO_DEST_FILE "words_info.txt"

int pow_cache[] = {1, 3, 9, 27, 81};

typedef struct Entropy {
    double H;
    char* word;
} Entropy;

typedef struct Tmp_word_list Tmp_word_list;
struct Tmp_word_list {
    Tmp_word_list* next;
    char* word;
};

void read_words(char* path, char*** words, int* nb_words) {
    FILE* file = fopen(path, "r");
    Tmp_word_list* tmp_words_list = NULL;
    *nb_words = 0;
    
    while(1) {
        Tmp_word_list* tmp = (Tmp_word_list*) malloc(sizeof(Tmp_word_list));
        tmp->word = (char*) malloc(sizeof(char) * WORD_LEN);

        if(fscanf(file, "word([") == EOF)
            break;

        for(int j = 0; j < WORD_LEN - 1; j++)
            fscanf(file, "%c, ", &(tmp->word[j]));

        fscanf(file, "%c]).\n", &(tmp->word[WORD_LEN - 1]));

        tmp->next = tmp_words_list;
        tmp_words_list = tmp;
        (*nb_words)++;
    }

    fclose(file);
    *words = (char**) malloc(sizeof(char*) * (*nb_words));

    for(int i = 0; i < (*nb_words); i++) {
        Tmp_word_list* current = tmp_words_list;
        (*words)[i] = current->word;
        tmp_words_list = current->next;
        free(current);
    }
}

char* concat_path(char* path1, char* path2) {
    int path1_len = strlen(path1);
    int path2_len = strlen(path2);
    int trailing_slash = 0;
    
    if(path1[path1_len - 1] == '/')
        trailing_slash = 1;

    char* new_path;
    
    if(trailing_slash) {
        new_path = (char*) malloc(sizeof(char) * (path1_len + path2_len + 1));
        sprintf(new_path, "%s%s", path1, path2);
    } else {
        new_path = (char*) malloc(sizeof(char) * (path1_len + path2_len + 2));
        sprintf(new_path, "%s/%s", path1, path2);
    }

    return new_path;
}

void write_words(char* dest_folder, char* words_path, char* info_path, Entropy* entropies, int nb_words) {
    char* wpath = concat_path(dest_folder, words_path);
    char* ipath = concat_path(dest_folder, info_path);
    FILE* words_file = fopen(wpath, "w");
    FILE* info_file = fopen(ipath, "w");
    
    for(int i = 0; i < nb_words; i++) {
        Entropy e = entropies[i];

        fprintf(words_file, "word([");

        for(int j = 0; j < WORD_LEN - 1; j++) {
            fprintf(words_file, "%c, ", e.word[j]);
            fprintf(info_file, "%c", e.word[j]);
        }

        fprintf(words_file, "%c]).\n", e.word[WORD_LEN - 1]);
        fprintf(info_file, "%c\t%f\n", e.word[WORD_LEN - 1], e.H);
    }

    free(wpath);
    free(ipath);
    fclose(words_file);
    fclose(info_file);
}

void free_words(char** words, int nb_words) {
    for(int i = 0; i < nb_words; i++) {
        free(words[i]);
    }

    free(words);
}

int get_pattern(char* soluce, char* word) {
    int* res = (int*) calloc(WORD_LEN, sizeof(int));
    int* used = (int*) calloc(WORD_LEN, sizeof(int));
    int value = 0;

    for(int i = 0; i < WORD_LEN; i++) {
        if (word[i] == soluce[i]) {
            res[i] = 2;
            used[i] = 1;
        }
    }

    for(int i = 0; i < WORD_LEN; i++) {
        if (res[i] != 0)
            continue;

        for(int j = 0; j < WORD_LEN; j++) {
            if(!used[j] && word[i] == soluce[j]) {
                res[i] = 1;
                used[j] = 1;
                break;
            }
        }
    }

    for(int i = 0; i < WORD_LEN; i++) {
        value += res[i] * pow_cache[i];
    }

    free(res);
    free(used);
    return value;
}

int pattern_match(char* word, int pattern, char* test) {
    if(get_pattern(test, word) == pattern)
    	return 1;
    
    return 0;
}

double entropy(char** words, int nb_words, int* match_table, char* word) {
    double H = 0.0;

    for(int i = 0; i < nb_words; i++) {
        int p = get_pattern(word, words[i]);
        match_table[p]++;
    }

    for(int i = 0; i < NB_PATTERNS; i++) {
        if(match_table[i] > 0) {
            double p = ((double) match_table[i]) / ((double) nb_words);
            H += -p * (log(p)/log(2));
        }

        match_table[i] = 0;
    }

    return H;
}

void progress_bar(int count, int total, struct timeval start_time, char* word, float H) {
    float ratio = ((float) count) / ((float) total);
    int filled_len = (int) floor(PROGRESS_BAR_SIZE * ratio);
    int empty_len = PROGRESS_BAR_SIZE - filled_len;

    struct timeval time_now;
    gettimeofday(&time_now, NULL);
    int time_diff = time_now.tv_sec - start_time.tv_sec;

    printf("\r[");

    for(int i = 0; i < filled_len; i++)
        printf("#");

    for(int i = 0; i < empty_len; i++)
        printf("-");

    printf("] %d/%d %.2ds - H(", count, total, time_diff);

    for(int i = 0; i < WORD_LEN; i++)
        printf("%c", word[i]);

    printf(") = %f", H);
    fflush(stdout);

    if(count == total)
        printf("\n");
}

void run_test() {
    printf("%s\n", concat_path(DEFAULT_DEST_FOLDER, INFO_DEST_FILE));
    printf("%s\n", concat_path("hello/hi", INFO_DEST_FILE));

    printf("%d == 242\n", get_pattern("abaca", "abaca"));
    printf("%d == 2\n", get_pattern("abaca", "axxxx"));
    printf("%d == 20\n", get_pattern("abaca", "axaxx"));
    printf("%d == 47\n", get_pattern("abaca", "axaax"));
    printf("%d == 0\n", get_pattern("abaca", "qxmoz"));
    printf("%d == 176\n", get_pattern("abaca", "aabaa"));
    printf("%d == 90\n", get_pattern("abide", "speed"));
    printf("%d == 37\n", get_pattern("erase", "speed"));
    printf("%d == 47\n", get_pattern("abaca", "arabe"));
    printf("%d == 23\n", get_pattern("arabe", "abaca"));
}

int get_args(int argc, char** argv, int* quiet, int* test, char** source_file, char** dest_folder) {
    for(int i = 1; i < argc; i++) {
        if(strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0) {
            printf("Usage: %s <options>\n", argv[0]);
            printf("\nOptions:\n");
            printf("-h, --help\t\tDisplay this help message\n");
            printf("--quiet\t\t\tHide execution messages\n");
            printf("--test\t\t\tRun tests\n");
            printf("-i, --input <file>\tPath to words source file (Prolog file) [default: '%s']\n", DEFAULT_SOURCE_FILE);
            printf("-o, --output <file>\tPath to folder where to put result files [default: '%s']\n", DEFAULT_DEST_FOLDER);
            return 2;
        }

        if(strcmp(argv[i], "--test") == 0) {
            *test = 1;
            return 0;
        }

        if(strcmp(argv[i], "--quiet") == 0) {
            *quiet = 1;
            continue;
        }

        if(strcmp(argv[i], "--input") == 0 || strcmp(argv[i], "-i") == 0) {
            if(i + 1 >= argc) {
                fprintf(stderr, "Missing value for %s\n", argv[i]);
                return 1;
            }

            *source_file = argv[i + 1];
            i++;
            continue;
        }

        if(strcmp(argv[i], "--output") == 0 || strcmp(argv[i], "-o") == 0) {
            if(i + 1 >= argc) {
                fprintf(stderr, "Missing value for %s\n", argv[i]);
                return 1;
            }

            *dest_folder = argv[i + 1];
            i++;
            continue;
        }

        fprintf(stderr, "Invalid option %s. Use --help for help\n", argv[i]);
        return 1;
    }

    return 0;
}

int main(int argc, char** argv) {
    int quiet = 0;
    int test = 0;
    char* source_file = DEFAULT_SOURCE_FILE;
    char* dest_folder = DEFAULT_DEST_FOLDER;
    int state = get_args(argc, argv, &quiet, &test, &source_file, &dest_folder);

    if(state == 1)
        return EXIT_FAILURE;
    else if(state != 0)
        return EXIT_SUCCESS;

    if(test) {
        run_test();
        return EXIT_SUCCESS;
    }

    int nb_words = 0;
    char** words;
    read_words(source_file, &words, &nb_words);

    int* match_table = (int*) calloc(NB_PATTERNS, sizeof(int));
    Entropy* entropies = (Entropy*) malloc(sizeof(Entropy) * nb_words);
    struct timeval tv_s, tv_e;

    gettimeofday(&tv_s, NULL);
    for(int i = 0; i < nb_words; i++) {
        double H = entropy(words, nb_words, match_table, words[i]);
        entropies[i].H = H;
        entropies[i].word = words[i];

        if(!quiet) {
            progress_bar(i + 1, nb_words, tv_s, words[i], H);
        }
    }

    for(int i = 0; i < nb_words; i++) {
        for(int j = i + 1; j < nb_words; j++) {
            if(entropies[i].H < entropies[j].H) {
                Entropy tmp = {.H = entropies[i].H, .word = entropies[i].word};
                entropies[i].H = entropies[j].H;
                entropies[i].word = entropies[j].word;
                entropies[j].H = tmp.H;
                entropies[j].word = tmp.word;
            }
        }
    }

    write_words(dest_folder, WORDS_DEST_FILE, INFO_DEST_FILE, entropies, nb_words);

    if(!quiet) {
        gettimeofday(&tv_e, NULL);
        printf("The program was run for %d words in %lds\n", nb_words, tv_e.tv_sec - tv_s.tv_sec);
    }

    free_words(words, nb_words);
    free(match_table);
    return EXIT_SUCCESS;
}
