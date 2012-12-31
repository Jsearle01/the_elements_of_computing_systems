from itertools import count

import os.path
import re

thisthat = {
        '0': 'THIS',
        '1': 'THAT',
        'this': 'THIS',
        'that': 'THAT',
        }

symbols = {
        'this': 'THIS',
        'that': 'THAT',
        'local'   : 'LCL',
        'argument': 'ARG',
        ('temp', '0') : 'R5',
        ('temp', '1') : 'R6',
        ('temp', '2') : 'R7',
        ('temp', '3') : 'R8',
        ('temp', '4') : 'R9',
        ('temp', '5') : 'R10',
        ('temp', '6') : 'R11',
        ('temp', '7') : 'R12',
        ('pointer', '0') : 'THIS',
        ('pointer', '1') : 'THAT',
        }

jumps = {
        'eq': 'JEQ',
        'lt': 'JGT',
        'gt': 'JLT',
        }

macro_aliases = {
        '++': 'increment',
        '--': 'decrement',
        '+=': 'increment_by',
        '-=': 'decrement_by',
        }

operators = {
        'neg' : '-',
        'not' : '!',
        'add' : '+',
        'sub' : '-',
        'and' : '&',
        'or' : '|',
        }

class CodeWriter:
    def __init__(self, output_file, stamp=False):
        self.file = output_file
        self.current_function = ''
        self.setup_global_functions()
        self.stamp = stamp

    def setup_global_functions(self):
        global asm
        asm = self.hlasm

        global unique_id
        unique_id = count().__next__

    def write(self, s):
        self.file.write(s)
        self.file.write('\n')

    def hlasm(self, s, *args, **kargs):
        lines = []
        for line in s.format(*args, **kargs).split('\n'):
            line = re.sub(r'\s*#.*', '', line).strip()
            if line != '':
                lines.append(line)

        for line in lines:
            if line[0] == ',': # macro
                cmd, *args = line[1:].strip().split()
                if cmd in macro_aliases:
                    cmd = macro_aliases[cmd]
                try:
                    getattr(self, 'macro_' + cmd)(*args)
                except AttributeError:
                    raise SyntaxError('macro not found: %s' % cmd)
            else:
                self.write(line)

    def setFileName(self, fileName):
        self.filename = os.path.splitext(os.path.basename(fileName))[0]

    def writeInit(self):
        asm('''
        ,stamp 0
        ,set SP 256
        ''')
        self.writeCall('Sys.init', '0')

    def writeLabel(self, label):
        asm('''
        ,stamp 1
        ({0}${1})
        ''', self.current_function, label)

    def writeGoto(self, label):
        asm('''
        ,stamp 2
        @{0}${1}
        0;JMP
        ''', self.current_function, label)

    def writeIf(self, label):
        asm('''
        ,stamp 3
        ,pop D
        @{0}${1}
        D;JNE
        ''', self.current_function, label)

    def writeCall(self, functionName, numArgs):
        asm('''
        ,stamp 4

        # push return-address
            ,set D return_{uid}
            ,push D
        # push LCL
            ,push *LCL
        # push ARG
            ,push *ARG
        # push THIS
            ,push *THIS
        # push THAT
            ,push *THAT
        # ARG=SP-n-5
            ,set ARG *SP
            ,-= ARG {numArgs}
            ,-= ARG 5
        # LCL=SP
            ,set LCL *SP
        # goto f
            ,goto {functionName}
        # (return-address)
            (return_{uid})
        ''',
        functionName = functionName,
        numArgs=numArgs,
        uid = unique_id()
        )

    def writeFunction(self, functionName, numLocals):
        self.current_function = functionName
        asm('''
        ({0})
        ,stamp 5
        ''', functionName)
        for i in range(int(numLocals)):
            asm(',push 0')

    def writeReturn(self):
        asm('''
        ,stamp 6
        # FRAME = LCL
            ,set {FRAME} *LCL
        # RET = *(FRAME-5)
            ,set {RET} *{FRAME}
            ,-= {RET} 5
            ,set {RET} **{RET}
        # *ARG = pop()
            ,pop D
            ,set *ARG D
        # SP = ARG+1
            ,set SP *ARG
            ,++ SP
        # THAT = *(FRAME-1)
            ,set THAT *{FRAME}
            ,-= THAT 1
            ,set THAT **THAT
        # THIS = *(FRAME-2)
            ,set THIS *{FRAME}
            ,-= THIS 2
            ,set THIS **THIS
        # ARG  = *(FRAME-3)
            ,set ARG *{FRAME}
            ,-= ARG 3
            ,set ARG **ARG
        # LCL  = *(FRAME-4)
            ,set LCL *{FRAME}
            ,-= LCL 4
            ,set LCL **LCL
        # goto RET
            ,goto *{RET}
        ''', FRAME='R13', RET='R14')

    def writeArithmetic(self, command):
        asm(',stamp 7')
        if command in ['neg', 'not']:
            # uses one argument
            asm('''
            @SP
            A=M-1
            M={}M
            ''', operators[command])
        elif command in ['eq', 'lt', 'gt']:
            # uses two arguments
            asm('''
            @SP
            M=M-1
            A=M
            D=M

            A=A-1
            D=D-M

            @{cmd}_TRUE_{id}
            D;{jump}
            D=0
            @{cmd}_END_{id}
            0;JMP
            ({cmd}_TRUE_{id})
            D=-1
            ({cmd}_END_{id})

            @SP
            A=M-1
            M=D
            ''',
            cmd=command.upper(),
            jump=jumps[command],
            id=unique_id())

        else:
            # uses two arguments
            asm('''
            @SP
            M=M-1
            A=M
            D=M
            A=A-1

            M=M{operator}D
            ''',
            operator = operators[command]
            )

    def writeBreakpoint(self, breakpoint_id):
        asm('''
        @{0}
        @{1}
        ''',
        23456,
        23400 + int(breakpoint_id)
        )

    def macro_pop(self, address):
        if address == 'D':
            asm('''
            ,-- SP
            A=M
            D=M
            ''')
        else:
            asm('''
            ,pop D
            @{0}
            M=D
            ''', address)

    def macro_push(self, address):
        if address in ['A', 'M']:
            asm('''
            D={}
            ,push D
            ''', address)
        elif address in ['D', '-1', '0', '1']:
            asm('''
            @SP
            M=M+1
            A=M-1
            M={}
            ''', address)
        else:
            asm('@{}', address.lstrip('*'))
            c = address.count('*')
            if c == 0:
                asm('D=A')
            elif c == 1:
                asm('D=M')
            else:
                for i in range(c - 1):
                    asm('A=M')
                asm('D=M')
            asm(',push D')

    def macro_stamp(self, id_number):
        if self.stamp:
            asm('''
            @{0}
            @{1}
            ''', 12345, 12300 + int(id_number))

    def macro_set(self, dest, source, offset=None):
        single_instruction = False

        if source in ['A', 'M', 'D', '-1', '0', '1']:
            single_instruction = True
            rhs = source
        elif source == '*A':
            single_instruction = True
            rhs = 'M'
        elif source == '*D':
            asm('''
            A=D
            D=M
            ''')
        elif source == '*M':
            asm('''
            A=M
            D=M
            ''')
        elif source[:2] == '[M':
            offset = offset[:-1]
            if offset == '0':
                single_instruction = True
                rhs = 'M'
            elif offset == '1':
                single_instruction = True
                rhs = 'M+1'
            else:
                asm('''
                D=M
                @{}
                D=D+A
                ''', offset)
        else:
            asm('@{}', source.lstrip('*'))
            try:
                while source[1] == '*':
                    asm('A=M')
                    source = source[1:]
            except IndexError:
                pass
            if source[0] == '*': asm('D=M')
            else:                asm('D=A')


        if single_instruction == False:
            rhs = 'D'


        if dest == 'D':
            pass
        elif dest == '*D':
            asm('''
            A=D
            A=M
            M={}
            ''', rhs)
        elif dest == 'A':
            asm('''
            A={}
            ''', rhs)
        elif dest == '*A':
            asm('''
            M={}
            ''', rhs)
        elif dest == 'M':
            asm('''
            M={}
            ''', rhs)
        elif dest == '*M':
            asm('''
            A=M
            M={}
            ''', rhs)
        else:
            asm('@{}', dest.lstrip('*'))
            while dest[0] == '*':
                asm('A=M')
                dest = dest[1:]
            asm('M={}', rhs)

    def macro_goto(self, address):
        asm('@{}', address.lstrip('*'))
        for i in range(address.count('*')):
            asm('A=M')
        asm('0;JMP')

    def macro_decrement(self, address):
        if address in ['D','A','M']:
            asm('{0}={0}-1', address)
        else:
            asm('''
            @{0}
            M=M-1
            ''', address)
        
    def macro_increment(self, address):
        if address in ['D','A','M']:
            asm('{0}={0}+1', address)
        else:
            asm('''
            @{0}
            M=M+1
            ''', address)

    def macro_decrement_by(self, address, amount):
        if amount == '0':
            pass
        elif amount == '1':
            self.macro_decrement(address)
        elif address == 'D':
            asm('''
            @{amount}
            D=D+A
            ''', amount=amount)
        elif address == 'A':
            asm('''
            D=A
            @{amount}
            A=D+A
            ''', amount=amount)
        elif address == 'M':
            raise SyntaxError('not implemented')
        else:
            asm('''
            @{1}
            D=A
            @{0}
            M=M-D
            ''', address, amount)

    def macro_increment_by(self, address, amount):
        if amount == '0':
            pass
        elif amount == '1':
            self.macro_increment(address)
        elif address == 'D':
            asm('''
            @{0}
            D=D+A
            ''', amount)
        elif address == 'A':
            asm('''
            D=A
            @{amount}
            A=D+A
            ''', amount=amount)
        elif address == 'M':
            asm('''
            # R13 = A 
                D=A
                @R13
                M=D

            # R14 = M
                A=D
                D=M
                @R14
                M=D

            @{amount}
            D=D+A
            @R13
            A=M
            M=D
            ''', amount=amount)
        else:
            asm('''
            @{1}
            D=M
            @{0}
            D=D+A
            M=M+D
            ''', address, amount)

    def WritePushPop(self, command, segment, index):
        if command == 'C_PUSH':
            asm(',stamp 8')
            if segment == 'constant':
                asm(',push {0}', index)

            elif segment == 'static':
                asm('''
                @{0}.{1}
                D=M
                ,push D
                ''', self.filename, index)

            elif segment in ['temp', 'pointer']:
                asm('''
                @{}
                D=M
                ,push D
                ''', symbols[(segment, index)])

            elif segment in ['this', 'that', 'argument', 'local']:
                asm('''
                @{}
                ,set A [M {}]
                D=M
                ,push D
                ''',
                symbols[segment],
                index)

            else:
                raise SyntaxError('unknown push sub command')

        elif command == 'C_POP':
            asm(',stamp 9')
            if segment == 'temp':
                asm('''
                @R5
                D=A
                ,+= D {0}
                @R13
                M=D
                ,pop D
                @R13
                A=M
                M=D
                ''', index)
            elif segment == 'static':
                asm('''
                ,pop D
                @{0}.{1}
                M=D
                ''', self.filename, index)
            elif segment == 'pointer':
                asm('''
                ,pop D
                @{}
                M=D
                ''', thisthat[index])
            elif segment in ['this', 'that']:
                asm('''
                @{0}
                D=M
                ,+= D {1}
                @R13
                M=D
                ,pop D
                @R13
                A=M
                M=D
                ''', thisthat[segment], index)
            else:
                asm('''
                ,set D *{symbol}
                ,+= D {index}
                ,set R13 D
                ,pop D
                ,set *R13 D
                ''', symbol=symbols[segment], index=index)
        else:
            raise SyntaxError('unknown pushPop: %s ; %s ; %s' % (command, segment, index))

    def writeHLASM(self, code):
        asm(code)

    def Close(self):
        self.file.close()

if __name__ == '__main__':
    print('hello')

