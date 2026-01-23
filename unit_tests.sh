#!/bin/sh

function unit_test() {
    F=$1; shift
    echo "################################################################################" >&2
    echo "# Testing [${F}]" >&2
    echo "################################################################################" >&2
    python3 "${F}"; RC=$?
    echo "################################################################################" >&2
    echo "# RC=[${RC}]" >&2
    echo "################################################################################" >&2
    echo  >&2
    return ${RC}
}

FinalRC=0
for F in *.py; do
    SKIP=0
    for S in "Solver" ""; do
        if [ "${F}" = "${S}.py" ]; then SKIP=1; break; fi
    done
    if [ ${SKIP} -eq 0 ]; then
        unit_test $F; RC=$?
        if [ ${RC} -ne 0 ]; then FinalRC=1; fi
    fi
done
if [ ${FinalRC} -ne 0 ]; then
    echo "FATAL: Some tests failed" >&2
    exit 1
fi
#exit 0