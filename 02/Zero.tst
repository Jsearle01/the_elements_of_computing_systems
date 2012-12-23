// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/02/HalfAdder.tst

load Zero.hdl,
output-file Zero.out,
compare-to Zero.cmp,
output-list a%B3.1.3 z%B3.1.3 out%B3.1.3;

set a 0,
set z 0,
eval,
output;

set a 0,
set z 1,
eval,
output;

set a 1,
set z 0,
eval,
output;

set a 1,
set z 1,
eval,
output;
