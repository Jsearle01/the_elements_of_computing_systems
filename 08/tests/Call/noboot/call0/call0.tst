load call0.asm,
output-file call0.out,
compare-to call0.cmp,
output-list
    RAM[0]%D1.6.1
    RAM[1]%D1.6.1
    RAM[2]%D1.6.1
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

repeat 100 {
  ticktock;
}

output;

