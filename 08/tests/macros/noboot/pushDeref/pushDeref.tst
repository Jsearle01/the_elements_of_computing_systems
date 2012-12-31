load pushDeref.asm,
output-file pushDeref.out,
compare-to pushDeref.cmp,
output-list
    RAM[0]%D1.6.1
    RAM[256]%D1.6.1
    RAM[257]%D1.6.1
    RAM[258]%D1.6.1
    RAM[259]%D1.6.1;

set RAM[0] 256,
set RAM[3] 200,
set RAM[200] 400,
set RAM[400] 600,
set RAM[600] 800,

repeat 100 {
  ticktock;
}

output;

