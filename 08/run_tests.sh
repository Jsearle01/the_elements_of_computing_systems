#! /usr/bin/env sh

function log () {
    echo `date "+%Y%m%d %H:%M:%S"` $* >> test_log.txt
}

function run_tests_in_dir() {
    for test in $1/* ; do
        if [[ -d $test ]]; then
            ./run.sh $test $2 &> .test.out

            if (( $? > 0 )); then
                log fail $test
                FAIL=$((FAIL+1))
                printf "%-18s : %s\n" `basename $test` $test | tee -a .test_fails
                echo
                cat .test.out
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

rm -f .test_fails
for tests in tests/* ; do
    run_tests_in_dir $tests/boot
    run_tests_in_dir $tests/noboot --no-bootstrap
done

TOTAL=$((PASS+FAIL))

echo Total: $TOTAL
echo Pass:  $PASS
echo Fail:  $FAIL
echo

if (($FAIL == 0)); then
    echo ALL PASSED
else
    echo Failed:
    cat .test_fails
fi

