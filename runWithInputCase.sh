#!/bin/bash

for ITEM in "$@"
    do
        printf "______Running input case $ITEM _________________"

        printf "\n\n"
        python3 Simplex/main.py < tests/cases/end2end/$ITEM 
        printf "\n\n" 
        printf "Input $ITEM ran, correct output is\n" 
        cat tests/cases/end2end/res-$ITEM &&
        printf "\n"

    done