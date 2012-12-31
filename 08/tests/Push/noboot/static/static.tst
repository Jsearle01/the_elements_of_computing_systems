load static.asm,
output-file static.out,
compare-to static.cmp,
output-list
    RAM[0]%D1.6.1
    RAM[1]%D1.6.1
    RAM[2]%D1.6.1
    RAM[256]%D1.6.1
    RAM[257]%D1.6.1
    RAM[258]%D1.6.1
    RAM[259]%D1.6.1
    RAM[260]%D1.6.1
    RAM[261]%D1.6.1;

set RAM[0] 256,
set RAM[1] 101,
set RAM[2] 102,
set RAM[3] 103,
set RAM[4] 104,

set RAM[16] 16,
set RAM[17] 17,

repeat 100 {
  ticktock;
}

output;

