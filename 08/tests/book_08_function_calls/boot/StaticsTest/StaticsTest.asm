@256
D=A
@SP
M=D
@return_0
D=A
@SP
M=M+1
A=M-1
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
@5
D=A
@ARG
M=M-D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(return_0)
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
(Class1.set)
@ARG
A=M
D=M
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
@Class1.0
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
@Class1.1
M=D
@SP
M=M+1
A=M-1
M=0
@VMReturn
0;JMP
(Class1.get)
@Class1.0
D=M
@SP
M=M+1
A=M-1
M=D
@Class1.1
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
M=M-D
@VMReturn
0;JMP
(Class2.set)
@ARG
A=M
D=M
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
@Class2.0
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
@Class2.1
M=D
@SP
M=M+1
A=M-1
M=0
@VMReturn
0;JMP
(Class2.get)
@Class2.0
D=M
@SP
M=M+1
A=M-1
M=D
@Class2.1
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
M=M-D
@VMReturn
0;JMP
(Sys.init)
@6
D=A
@SP
M=M+1
A=M-1
M=D
@8
D=A
@SP
M=M+1
A=M-1
M=D
@return_1
D=A
@SP
M=M+1
A=M-1
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
@7
D=A
@ARG
M=M-D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(return_1)
@SP
M=M-1
A=M
D=M
@R5
M=D
@23
D=A
@SP
M=M+1
A=M-1
M=D
@15
D=A
@SP
M=M+1
A=M-1
M=D
@return_2
D=A
@SP
M=M+1
A=M-1
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
@7
D=A
@ARG
M=M-D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(return_2)
@SP
M=M-1
A=M
D=M
@R5
M=D
@return_3
D=A
@SP
M=M+1
A=M-1
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
@5
D=A
@ARG
M=M-D
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(return_3)
@return_4
D=A
@SP
M=M+1
A=M-1
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
@5
D=A
@ARG
M=M-D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(return_4)
(Sys.init$WHILE)
@Sys.init$WHILE
0;JMP
