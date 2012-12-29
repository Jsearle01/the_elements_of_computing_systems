#! /usr/bin/env sh

FILE=$1/`basename $1`

./VMtranslator.py $1
if (($? != 0)); then
    exit
fi

cpuemu $FILE.tst
if (($? != 0)); then
    cat $FILE.vm
    echo
    cat $FILE.cmp
    echo "\n====\n"
    cat $FILE.out
    exit
fi

