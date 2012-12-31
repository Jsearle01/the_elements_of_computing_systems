load this.asm,
output-file this.out,
compare-to this.cmp,
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
set RAM[4] 106,

set RAM[103] 333,
set RAM[104] 444,
set RAM[105] 555,
set RAM[106] 666,
set RAM[107] 777,
set RAM[108] 888,


repeat 100 {
  ticktock;
}

output;

