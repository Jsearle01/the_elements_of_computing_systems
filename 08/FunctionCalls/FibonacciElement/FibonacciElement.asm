@12345
@12300
@256
D=A
@SP
M=D
@Sys.init
0;JMP
(Main.fibonacci)
@12345
@12305
@12345
@12308
@ARG
D=M
@0
D=D+A
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
@12345
@12308
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@12345
@12307
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@LT_TRUE_0
D;JGT
D=0
@LT_END_0
0;JMP
(LT_TRUE_0)
D=-1
(LT_END_0)
@SP
A=M
M=D
@SP
M=M+1
@12345
@12303
@SP
M=M-1
A=M
D=M
@Main.fibonacci$IF_TRUE
D;JNE
@12345
@12302
@Main.fibonacci$IF_FALSE
0;JMP
@12345
@12301
(Main.fibonacci$IF_TRUE)
@12345
@12308
@ARG
D=M
@0
D=D+A
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
@12345
@12306
@LCL
D=M
@R13
M=D
@R13
D=M
@R14
M=D
@5
D=A
@R14
M=M-D
@R14
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
@SP
M=M+1
@R13
D=M
@THAT
M=D
@THAT
M=M-1
@THAT
A=M
D=M
@THAT
M=D
@R13
D=M
@THIS
M=D
@2
D=A
@THIS
M=M-D
@THIS
A=M
D=M
@THIS
M=D
@R13
D=M
@ARG
M=D
@3
D=A
@ARG
M=M-D
@ARG
A=M
D=M
@ARG
M=D
@R13
D=M
@LCL
M=D
@4
D=A
@LCL
M=M-D
@LCL
A=M
D=M
@LCL
M=D
@R14
A=M
0;JMP
@12345
@12301
(Main.fibonacci$IF_FALSE)
@12345
@12308
@ARG
D=M
@0
D=D+A
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
@12345
@12308
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@12345
@12307
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
@12345
@12304
@return_1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@ARG
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@THIS
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@THAT
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@ARG
M=D
@ARG
M=M-1
@5
D=A
@ARG
M=M-D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(return_1)
@12345
@12308
@ARG
D=M
@0
D=D+A
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
@12345
@12308
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@12345
@12307
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
@12345
@12304
@return_2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@ARG
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@THIS
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@THAT
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@ARG
M=D
@ARG
M=M-1
@5
D=A
@ARG
M=M-D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(return_2)
@12345
@12307
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
@12345
@12306
@LCL
D=M
@R13
M=D
@R13
D=M
@R14
M=D
@5
D=A
@R14
M=M-D
@R14
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
@SP
M=M+1
@R13
D=M
@THAT
M=D
@THAT
M=M-1
@THAT
A=M
D=M
@THAT
M=D
@R13
D=M
@THIS
M=D
@2
D=A
@THIS
M=M-D
@THIS
A=M
D=M
@THIS
M=D
@R13
D=M
@ARG
M=D
@3
D=A
@ARG
M=M-D
@ARG
A=M
D=M
@ARG
M=D
@R13
D=M
@LCL
M=D
@4
D=A
@LCL
M=M-D
@LCL
A=M
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Sys.init)
@12345
@12305
@12345
@12308
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
@12345
@12304
@return_3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@ARG
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@THIS
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@THAT
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@ARG
M=D
@ARG
M=M-1
@5
D=A
@ARG
M=M-D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(return_3)
@12345
@12301
(Sys.init$WHILE)
@12345
@12302
@Sys.init$WHILE
0;JMP
