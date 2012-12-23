// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/02/Add16.tst

load Zero16.hdl,
output-file Zero16.out,
compare-to Zero16.cmp,
output-list a%B1.16.1 z%B1.1.1 out%B1.16.1;

set a %B0000000000000000,
set z 0,
eval,
output;

set a %B0000000000000000,
set z 1,
eval,
output;

set a %B1111111111111111,
set z 0,
eval,
output;

set a %B1010101010101010,
set z 1,
eval,
output;

set a %B0011110011000011,
set z 0,
eval,
output;

set a %B0001001000110100,
set z 1,
eval,
output;

