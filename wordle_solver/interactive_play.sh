#!/bin/bash

WORD_SIZE=5
NB_TRIES=6
WORDS_FILE="save/word.pl"
SOLVER_FILE="solver.pl"
WORD_PROMPT_REGEX_PARSER="^.*P = \[\([a-z]\), \([a-z]\), \([a-z]\), \([a-z]\), \([a-z]\)\].*$"
WORD_REGEX_PARSER="^\([a-z]\)\([a-z]\)\([a-z]\)\([a-z]\)\([a-z]\)$"
WORD_REGEX="^[a-z]{5}$"
RESULT_REGEX="^[gGoObB]{5}$"

function word_to_list() {
    echo "$1" | sed "s/$WORD_REGEX_PARSER/[\1, \2, \3, \4, \5]/"
}

function pattern_letter_to_word() {
    echo "$1" | sed "s/g/green/g" | sed "s/o/orange/g" | sed "s/b/black/g"
}

function colorize_letter() {
    if [[ "$2" == "g" ]]; then
        echo -e "\033[32m$1\033[37m"
    elif [[ "$2" == "o" ]]; then
        echo -e "\033[33m$1\033[37m"
    else
        echo -e "\033[37m$1\033[37m"
    fi
}

function print_game() {
    for (( r = 1; r <= $NB_TRIES; r++ )); do
        line=$(echo -e "$1" | sed -n "${r}p")
        read word pattern <<< $(echo -e "$line")
        
        echo "+---+---+---+---+---+"
        for (( c = 0; c < $WORD_SIZE; c++ )); do
            l=" "

            if [[ "$word" != "" ]]; then
                l="${word:$c:1}"
                l="${l^^}"
                l=$(colorize_letter "$l" "${pattern:$c:1}")
            fi
            
            echo -n "| $l "
        done
        echo "|"

    done
    echo "+---+---+---+---+---+"
}

function suggest() {
    OS=""
    CS=""

    if [[ "$1" != "" ]]; then
        while IFS=" " read word pattern; do
            O=$(word_to_list "$word")
            C=$(word_to_list "$pattern")
            C=$(pattern_letter_to_word "$C")

            if [[ "$OS" != "" ]]; then
                OS="$OS, "
                CS="$CS, "
            fi

            OS="$OS$O"
            CS="$CS$C"
        done <<< $(echo -e "$1")
    fi

    prompt_out=$(echo -e "
        consult(\"$WORDS_FILE\").
        consult(\"$SOLVER_FILE\").
        suggest(P, [$OS], [$CS]).
    " | prolog --quiet)

    word=$(echo $prompt_out | sed "s/$WORD_PROMPT_REGEX_PARSER/\1\2\3\4\5/")

    if [[ ! "$word" =~ $WORD_REGEX ]]; then
        return 1
    fi

    echo "$word"
    return 0
}

function validate_result() {
    if [[ ! "$1" =~ $RESULT_REGEX ]]; then
        return 1
    fi

    return 0
}

function read_result() {
    while :; do
        read -p "Enter result: " res
        res=$(echo "$res" | sed "s/^\s*\(.*\)\s*$/\1/")
        validate_result "$res"

        if [[ $? -eq 0 ]]; then
            break
        fi
    done

    echo "$res"
}

suggests=""

for (( i = 0; i < $NB_TRIES; i++ )); do
    clear

    print_game "$suggests"
    s=$(suggest "$suggests")

    if [[ $? -ne 0 ]]; then
        echo "No more suggestion available..."
        break
    fi

    echo "Suggest: ${s^^}"
    c=$(read_result)

    suggests="$suggests$s $c\n"

    if [[ "$c" == "ggggg" ]]; then
        clear
        print_game "$suggests"
        break
    fi
done