#! /usr/bin/env sh

lhs=`basename $1`
rhs=$2

if [[ -d $rhs ]]; then
    echo $rhs already exists
    exit 1
fi

cp -r $lhs $rhs
rename -e "s/$lhs/$rhs/" $rhs/*
sed -i .tmp -e "s/$lhs/$rhs/" $rhs/*.tst
if (( $? == 0 )) ; then
    rm $rhs/*.tst.tmp
fi

