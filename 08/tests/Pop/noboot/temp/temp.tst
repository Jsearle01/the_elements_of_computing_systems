load temp.asm,
output-file temp.out,
compare-to temp.cmp,
output-list
    RAM[0]%D1.6.1
    RAM[1]%D1.6.1
    RAM[2]%D1.6.1
    RAM[3]%D1.6.1
    RAM[4]%D1.6.1
    RAM[5]%D1.6.1
    RAM[6]%D1.6.1
    RAM[7]%D1.6.1
    RAM[102]%D1.6.1
    RAM[103]%D1.6.1
    RAM[104]%D1.6.1
    RAM[105]%D1.6.1
    RAM[106]%D1.6.1
    RAM[107]%D1.6.1;

set RAM[0] 259,
set RAM[1] 102,
set RAM[2] 103,
set RAM[3] 104,
set RAM[4] 105,
set RAM[5] 555,
set RAM[6] 666,
set RAM[7] 777,

set RAM[102] 102,
set RAM[103] 103,
set RAM[104] 104,
set RAM[105] 105,
set RAM[106] 106,
set RAM[107] 107,

set RAM[256] 56,
set RAM[257] 57,
set RAM[258] 58,

repeat 100 {
  ticktock;
}

output;

