#! /usr/bin/env sh

FILE=$1/`basename $1`

./VMtranslator.py $*
if (($? != 0)); then
    exit
fi

cpuemu $FILE.tst
if (($? != 0)); then
    cat $1/*.vm
    echo
    cat $1/*.cmp
    echo "\n====\n"
    cat $1/*.out
    echo
    cpuemu $FILE.tst
    exit
fi

