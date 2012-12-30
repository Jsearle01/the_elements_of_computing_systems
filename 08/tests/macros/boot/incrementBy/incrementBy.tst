load incrementBy.asm,
output-file incrementBy.out,
compare-to incrementBy.cmp,
output-list
    D%D1.6.1
    RAM[0]%D1.6.1
    RAM[256]%D1.6.1
    RAM[257]%D1.6.1
    RAM[258]%D1.6.1;

set RAM[0] 256,
set RAM[13] 0,
set RAM[14] 0,

repeat 2500 {
  ticktock;
}

output;

