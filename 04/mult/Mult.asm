// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[3], respectively.)

// Put your code here.

// zero R2
@R2
M=0

// i = R0
@R0
D=M
@i
M=D  // *i=D

(LOOP)
    // check if loop is over
    @i   // read R0 into A register
    D=M   // dereference A into D register
    @END  // set Jump destination
    D;JEQ // jump if D == 0
    
    // increase R2 by R1
    @R1   // A=R1
    D=M   // D=*A
    @R2   // A=R2
    M=M+D // *A += D

    // decrement i
    @i    // A=i
    M=M-1 // *a -= 1

    @LOOP // set jump destination
    0;JMP // jump

(END)
    @END
    0;JMP

