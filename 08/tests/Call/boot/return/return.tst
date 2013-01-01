load return.asm,
output-file return.out,
compare-to return.cmp,
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

set RAM[0] 0,
set RAM[1] 0,
set RAM[2] 0,

set RAM[256] 6,
set RAM[257] 7,
set RAM[258] 8,
set RAM[259] 9,
set RAM[260] 0,

repeat 200 {
  ticktock;
}

output;

