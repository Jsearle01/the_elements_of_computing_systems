// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/02/HalfAdder.tst

load Negate.hdl,
output-file Negate.out,
compare-to Negate.cmp,
output-list a%B3.1.3 n%B3.1.3 out%B3.1.3;

set a 0,
set n 0,
eval,
output;

set a 0,
set n 1,
eval,
output;

set a 1,
set n 0,
eval,
output;

set a 1,
set n 1,
eval,
output;

