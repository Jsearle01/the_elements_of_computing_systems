@SP
A=M
M=0
@SP
M=M+1
@LCL
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
($LOOP_START)
@ARG
D=M
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D+M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@ARG
D=M
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=-D
D=D+M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@ARG
D=M
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@$LOOP_START
D;JNE
@LCL
D=M
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
