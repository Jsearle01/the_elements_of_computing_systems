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

set RAM[0] 261,
set RAM[1] 261,
set RAM[2] 256,

set RAM[256] 200,
set RAM[257] 101,
set RAM[258] 102,
set RAM[259] 103,
set RAM[260] 104,

repeat 100 {
  ticktock;
}

output;

