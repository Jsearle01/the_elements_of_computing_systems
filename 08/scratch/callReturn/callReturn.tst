load callReturn.asm,
output-file callReturn.out,
compare-to callReturn.cmp,
output-list
    RAM[0]%D1.6.1
    RAM[1]%D1.6.1
    RAM[2]%D1.6.1
    RAM[3]%D1.6.1
    RAM[4]%D1.6.1
    RAM[256]%D1.6.1;

set RAM[0] 256,
set RAM[1] 1,
set RAM[2] 2,
set RAM[3] 3,
set RAM[4] 4,

repeat 2500 {
  ticktock;
}

output;

