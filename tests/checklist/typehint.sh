#!/bin/bash

# shellcheck source=tests/checklist/base.sh
. "$(dirname ${BASH_SOURCE[0]})/base.sh"

echo -e "$YELLOW> Checking type hints...$RESET"

mypy compressor/

check $? "Type hinting"
