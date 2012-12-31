load popD.asm,
output-file popD.out,
compare-to popD.cmp,
output-list
    D%D1.6.1
    RAM[0]%D1.6.1
    RAM[256]%D1.6.1
    RAM[257]%D1.6.1
    RAM[258]%D1.6.1;

set A 2,
set RAM[0] 257,
set RAM[256] 69,

repeat 100 {
  ticktock;
}

output;

