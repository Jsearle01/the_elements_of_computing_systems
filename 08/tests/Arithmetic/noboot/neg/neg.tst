load neg.asm,
output-file neg.out,
compare-to neg.cmp,
output-list
    D%D1.6.1
    RAM[0]%D1.6.1
    RAM[256]%D1.6.1
    RAM[257]%D1.6.1
    RAM[258]%D1.6.1;

set RAM[0] 257,
set RAM[256] 5,

repeat 100 {
  ticktock;
}

output;

