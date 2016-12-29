#!/usr/bin/env bash

# Time limit for command to execute
TIMEOUT_SEC=3


if [ "$#" -lt 3 ] || [[ $@ != *"@@"* ]]; then
    echo "Usage: $0 <testcase directory> <command with args>"
    echo ""
    echo "Replace filename in command with @@"
    exit -1
fi

TESTCASES=$1

function join_by { local IFS="$1"; shift; echo "$*"; }

set -- "${@:2}"
CMD=$(join_by " " $@)

for SAMPLE in $(find $TESTCASES -type f); do
    echo $SAMPLE

    S_CMD="timeout 3 ${CMD/@@/$SAMPLE}"
    OUT=$($S_CMD 2>&1)

    # Check for ASAN Output
    if [[ $OUT = *Sanitizer* ]]; then
        # Send to 2nd stage processor
        python asan_parse.py asan-output-full.csv "${S_CMD}"
    fi
done
