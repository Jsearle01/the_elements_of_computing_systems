#! /usr/bin/env sh

rm -f test/*/*[^T].xml

for source in test/*/*.jack; do
    ./JackAnalyzer.py $source
    out=${source/.jack/.xml}
    ref=orig/${out#*/*}
    diff $out $ref > /dev/null
    if (( $? != 0 )); then
        vimdiff $out $ref
    fi
done

