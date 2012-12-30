#! /usr/bin/env sh

function log () {
    echo `date "+%Y%m%d %H:%M:%S"` $* >> test_log.txt
}

function run_tests() {
    for test in $1/* ; do
        if [[ -d $test ]]; then
            ./run.sh $test $2 > .test.out
            if (( $? > 0 )); then
                log fail $test
                FAIL=$((FAIL+1))
                echo fail: $test
                echo
                cat .test.out
                echo
                echo
            else
                log pass $test
                PASS=$((PASS+1))
            fi
        fi
    done
}

PASS=0
FAIL=0

for tests in tests/* ; do
    run_tests $tests/boot
    run_tests $tests/noboot --no-bootstrap
done

exit

TOTAL=$((PASS+FAIL))

echo Total: $TOTAL
echo Pass:  $PASS
echo Fail:  $FAIL
echo

if (($FAIL == 0)); then
    echo ALL PASSED
else
    echo Fails
fi

