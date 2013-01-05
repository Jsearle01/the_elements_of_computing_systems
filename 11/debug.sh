#! /usr/bin/env sh

# rm -f test/*/*[^T].xml

rm -rf temp/*

if [[ ! -d temp ]]; then
    mkdir temp
fi

cp -r tests temp
mv temp/tests temp/ref
cp -r tests temp
mv temp/tests temp/new

for ref in temp/ref/*; do
    jackc $ref

    new=${ref/ref/new}
    ./JackCompiler.py $new
done

for refFile in temp/ref/*/*.vm; do
    newFile=${refFile/ref/new}

    diff $refFile $newFile > /dev/null
    if (( $? != 0 )); then
        jackFile=${newFile/.vm/.jack}
        ./JackCompiler.py $jackFile --debug --stdout | less
        exit
    fi
done

