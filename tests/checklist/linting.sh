#!/bin/bash

# shellcheck source=tests/checklist/base.sh
. "$(dirname ${BASH_SOURCE[0]})/base.sh"

echo -e "$YELLOW> Checking code style...$RESET"
pylint --rcfile=setup.cfg \
    compressor/ \
    tests/

check $? "Code style"
