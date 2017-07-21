#!/bin/bash

readonly RESULTS="perfornance-results.rst"
readonly TEST_FILE="/tmp/compressed.zf"
readonly SAMPLE_FILE="/usr/share/dict/words"

rm -f $RESULTS

date --rfc-3339=seconds >> $RESULTS
echo "^^^^^^^^^^^^^^^^^^^^^^^^^" >> $RESULTS

python --version >> $RESULTS

sample_run() {
    pycompress -c $SAMPLE_FILE -d $TEST_FILE
}


latency() {
    echo "Checking latency on first run..."
    time sample_run 2&> $RESULTS
}


latency
