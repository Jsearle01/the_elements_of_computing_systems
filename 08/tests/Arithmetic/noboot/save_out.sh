#! /usr/bin/env sh

if [[ -d $1 ]]; then
    cp $1/*.out $1/*.cmp
fi

