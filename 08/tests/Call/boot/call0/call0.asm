@256
D=A
@SP
M=D
@RETURN_0
D=A
@SP
M=M+1
A=M-1
M=D
@Sys.init
D=A
@SP
M=M+1
A=M-1
M=D
@5
D=A
@SP
M=M+1
A=M-1
M=D
@VMCall
0;JMP
(RETURN_0)
(END)
@END
0;JMP
(VMReturn)
@LCL
D=M
@R13
M=D
@R14
M=D
@5
D=A
@R14
M=M-D
A=M
D=M
@R14
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D
M=M+1
@R13
M=M-1
A=M
D=M
@THAT
M=D
@R13
M=M-1
A=M
D=M
@THIS
M=D
@R13
M=M-1
A=M
D=M
@ARG
M=D
@R13
M=M-1
A=M
D=M
@LCL
M=D
@R14
A=M
0;JMP
(VMCall)
@SP
M=M-1
A=M
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R14
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@ARG
M=D
@R13
D=M
@ARG
M=M-D
@SP
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Sys.init)
@2
D=A
@SP
M=M+1
A=M-1
M=D
@3
D=A
@SP
M=M+1
A=M-1
M=D
@RETURN_1
D=A
@SP
M=M+1
A=M-1
M=D
@Sys.testFunc
D=A
@SP
M=M+1
A=M-1
M=D
@7
D=A
@SP
M=M+1
A=M-1
M=D
@VMCall
0;JMP
(RETURN_1)
@VMReturn
0;JMP
(Sys.testFunc)
@ARG
A=M
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
A=M+1
D=M
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D
@VMReturn
0;JMP
