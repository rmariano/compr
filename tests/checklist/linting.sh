#!/bin/bash

YELLOW="\e[93m"
RED="\e[91m"
RESET="\e[0m"
TICK="\e[32m✔"
CROSS="\e[31m✘"

echo -e "$YELLOW> Checking code style...$RESET"
pylint --rcfile=setup.cfg \
    compressor/ \
    tests/

if [[ "$?" == "0" ]]; then
    echo -e "$TICK Code style correct$RESET"
else
    echo -e "$CROSS Check for errors in the code style$RESET"
fi
