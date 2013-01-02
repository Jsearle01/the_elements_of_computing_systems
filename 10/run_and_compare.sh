#! /usr/bin/env sh

rm -f test/*/*T.xml

for source in test/*/*.jack; do
    ./JackTokenizer.py $source
    out=${source/.jack/T.xml}
    ref=orig/${out#*/*}
    diff $out $ref > /dev/null
    if (( $? != 0 )); then
        echo failed: $source
    fi
done

