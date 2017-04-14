#!/bin/bash
export YELLOW="\e[93m"
export RED="\e[91m"
RESET="\e[0m"
TICK="\e[32m✔"
CROSS="\e[31m✘"


check() {
    ######
    ## Print the messages according to a generic verification
    ## and return the exit code
    ## $1: The exit code of the program that was invoked
    ## $2: The name of the task being run
    ######

    if [[ "$1" == "0" ]]; then
        echo -e "$TICK $2 passed$RESET"
    else
        echo -e "$CROSS Check for errors in $2 $RESET"
        exit 1
    fi
}
