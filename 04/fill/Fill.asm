// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.


(LOOP)
    @KBD // A=24576
    D=M    // D=*A
    @BLACK
    D;JGT
    //WHITE
    @bit
    M=0
    @COLOR_END
    0;JMP

    (BLACK)
    @bit
    M=-1

    (COLOR_END)

    // i=512 {
        @8192
        D=A
        @i
        M=D
    // }

    // screen_pointer = SCREEN
        @SCREEN
        D=A
        @screen_pointer
        M=D

    (FILL_LOOP)
    // body {
        @bit
        D=M
        @screen_pointer
        A=M
        M=D
    // }

    // step {
        @i
        M=M-1

        @screen_pointer
        M=M+1
    // }

    // if i > 0 then jump {
        @i
        D=M
        @FILL_LOOP
        D;JGT
    // }

    @LOOP
    0;JMP
    
    (END)
    @END
    0;JMP
