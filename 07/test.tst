// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/07/StackArithmetic/StackTest/StackTest.tst

load test.asm,
output-file test.out,
compare-to test.cmp,
output-list RAM[0]%D2.6.2 RAM[256]%D2.6.2 RAM[257]%D2.6.2 
            RAM[258]%D2.6.2 RAM[259]%D2.6.2;

set RAM[0] 256,
set RAM[1] 300,
set RAM[2] 400,
set RAM[3] 3000,
set RAM[4] 3010,
set RAM[256] 0,
set RAM[257] 0,
set RAM[258] 0,
set RAM[259] 0,

repeat 200 {
  ticktock;
}

output;

