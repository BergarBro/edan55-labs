#!/bin/bash
R0_test=("g30.in" "g40.in" "g50.in" "g60.in")
R1_test=("g30.in" "g40.in" "g50.in" "g60.in" "g70.in" "g80.in" "g90.in" "g100.in")
R2_test=("g30.in" "g40.in" "g50.in" "g60.in" "g70.in" "g80.in" "g90.in" "g100.in" "g110.in" "g120.in")
R3_test=("g130.in")

if [ "$1" = "r0" ]; then
    tests=("${R0_test[@]}")
    program="r0.py"
elif [ "$1" = "r1" ]; then
    tests=("${R1_test[@]}")
    program="r1.py"
elif [ "$1" = "r2" ]; then
    tests=("${R2_test[@]}")
    program="r2.py"
elif [ "$1" = "r3" ]; then
    tests=("${R3_test[@]}")
    program="r2.py"
else
    echo "Usage: ./test.sh r0|r1|r2|r3"
    exit 1
fi

for file in "${tests[@]}"
do
    if [ "$2" != "plot" ]; then
        echo "Running $program on $file"
    fi
    read n max_size rec_calls log_rec_calls <<< $( python "$program" < "data/$file")
    if [ "$2" = "plot" ]; then
        echo "(${n}, ${log_rec_calls})"
    else
        echo "Size of Independant Set: ${max_size}"
        echo "Number of recusive calls: ${rec_calls}"
        echo ""
    fi
done