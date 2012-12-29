from itertools import count
from functools import partial

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
        }

macro_aliases = {
        '++': 'increment',
        '--': 'decrement',
        '+=': 'increment_by',
        '-=': 'decrement_by',
        }

class CodeWriter:
    def __init__(self, output_file):
        global asm
        asm = self.hlasm
        self.file = output_file
        self.get_id = count().__next__
        self.current_function = ''

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
        ''')

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
        # push LCL
        # push ARG
        # push THIS
        # push THAT
        # ARG=SP-n-5
        # LCL=SP
        # goto f
        # (return-address)
        ''')

    def writeFunction(self, functionName, numLocals):
        asm('''
        ,stamp 5
        ({0})
        ''', functionName)
        for i in range(int(numLocals)):
            asm(',push constant 0')

    def writeReturn(self):
        asm('''
        ,stamp 6
        # FRAME = LCL
        ,set R13 LCL
        # RET = *(FRAME-5)
        ,set R14 R13
        ,-= R14 5
        ,set R15 *R14
        # *ARG = pop()
        ,pop D
        set *ARG D
        # SP = ARG+1
        ,set D ARG
        ,+= D 1
        ,set SP D
        # THAT = *(FRAME-1)
        # THIS = *(FRAME-2)
        # ARG  = *(FRAME-3)
        # LCL  = *(FRAME-4)
        # goto RET
        ,goto R15
        ''')

    def writeArithmetic(self, command):
        asm(',stamp 7')
        if command == 'neg':
            asm('''
            ,pop D
            D=-D
            ,push D
            ''')
        elif command == 'not':
            asm('''
            ,pop D
            D=!D
            ,push D
            ''')
        elif command == 'eq':
            asm('''
            ,pop D
            ,-- SP
            A=M
            D=D-M
            @EQ_TRUE_{0}
            D;JEQ
            D=0
            @EQ_END_{0}
            0;JMP
            (EQ_TRUE_{0})
            D=-1
            (EQ_END_{0})
            ,push D
            ''', self.get_id())
        elif command == 'gt':
            asm('''
            ,pop D
            ,-- SP
            A=M
            D=D-M
            @GT_TRUE_{0}
            D;JLT
            D=0
            @GT_END_{0}
            0;JMP
            (GT_TRUE_{0})
            D=-1
            (GT_END_{0})
            ,push D
            ''', self.get_id())
        elif command == 'lt':
            asm('''
            ,pop D
            ,-- SP
            A=M
            D=D-M
            @LT_TRUE_{0}
            D;JGT
            D=0
            @LT_END_{0}
            0;JMP
            (LT_TRUE_{0})
            D=-1
            (LT_END_{0})
            ,push D
            ''', self.get_id())

        else:
            asm('''
            ,pop D
            ,-- SP
            A=M
            ''')

            if   command == 'add': asm('D=D+M')
            elif command == 'sub': asm('D=-D\nD=D+M')
            elif command == 'and': asm('D=D&M')   # D &= *SP
            elif command == 'or' : asm('D=D|M')   # D |= *SP
            else: asm('arithmetic: %s' % command)

            asm(',push D')

    def macro_pop(self, dest):
        if dest == 'D':
            asm('''
            ,-- SP
            A=M
            D=M
            ''')
        else:
            raise Error('unknown pop destination')

    def macro_push(self, source, value=None):
        if source == 'D':
            asm(',set *SP D')
            asm(',++ SP')
        elif source == 'constant':
            asm('''
            @{0}
            D=A
            ,push D
            ''', value)
        else:
            raise Error('unknown push destination')

    def macro_stamp(self, id_number):
        asm('''
        @{0}
        @{1}
        ''', 12345, 12300 + int(id_number))

    def macro_set(self, dest, source):
        # set D to source
        if source == 'D':
            pass
        elif source == '*D':
            asm('''
            A=D
            D=M
            ''')
        elif source == 'A':
            asm('''
            D=A
            ''')
        elif source == '*A':
            asm('''
            D=M
            ''')
        elif source == 'M':
            asm('''
            D=M
            ''')
        elif source == '*M':
            asm('''
            A=M
            D=M
            ''')
        else:
            asm('@{}', source)
            if source[0] == '*': asm('D=M')
            else:                asm('D=A')

        if dest == 'D':
            pass
        elif dest == '*D':
            asm('''
            A=D
            A=M
            M=D
            ''')
        elif dest == 'A':
            asm('''
            A=D
            ''')
        elif dest == '*A':
            asm('''
            M=D
            ''')
        elif dest == 'M':
            asm('''
            M=D
            ''')
        elif dest == '*M':
            asm('''
            A=M
            M=D
            ''')
        else:
            if dest[0] == '*':
                asm('''
                @{}
                A=M
                M=D
                ''', dest[1:])
            else:
                asm('''
                @{}
                M=D
                ''', dest)

    def macro_goto(self, address):
        asm('''
        @{}
        0;JMP
        ''', address)

    def macro_decrement(self, symbol):
        asm('''
        @{0}
        M=M-1
        ''', symbol)
        
    def macro_increment(self, address):
        asm('''
        @{0}
        M=M+1
        ''', address)

    def macro_decrement_by(self, address, amount):
        if amount == 1:
            macro_decrement(address)
        else:
            asm('''
            @{1}
            D=A
            A{0}
            M=M-D
            ''', address, amount)

    def macro_increment_by(self, address, amount):
        if amount == 1:
            macro_increment(address)
        else:
            asm('''
            @{1}
            D=A
            A{0}
            M=M+D
            ''', address, amount)

    def store_segment_pointer(self, dest, segment, index):
        asm('''
        @{0}

        # increment pointer by index
        D=M
        @{1}
        D=D+A

        # store pointer
        @{2}
        M=D
        ''', symbols[segment], index, dest)
            
    def WritePushPop(self, command, segment, index):
        asm('''
        ,stamp 8
        ''')
        if command == 'C_PUSH':
            if segment == 'constant':
                asm(',push constant {0}', index)
            elif segment == 'static':
                asm('''
                @{0}.{1}
                D=M
                ,push D
                ''', self.filename, index)
            elif segment == 'temp':
                # push temp index -> onto the stack
                asm('''
                @R5
                D=A
                @{0}
                D=D+A
                A=D
                D=M
                ,push D
                ''', index)
            elif segment == 'pointer':
                if index == '0':
                    dest = 'THIS'
                else:
                    dest = 'THAT'
                asm('''
                @{}
                D=M
                ,push D
                ''', dest)
            elif segment == 'this' or segment == 'that':
                asm('''
                @{0}
                D=M
                @{1}
                D=D+A
                A=D
                D=M
                ,push D
                ''', segment.upper(), index)
            else:
                self.store_segment_pointer('R13', segment, index)
                self.hlasm('''
                @R13
                A=M
                D=M
                ,push D
                ''')
        elif command == 'C_POP':
            if segment == 'temp':
                asm('''
                @R5
                D=A
                @{0}
                D=D+A
                @R13
                M=D
                ,pop D
                @R13
                A=M
                M=D
                '''. index)
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
                @{1}
                D=D+A
                @R13
                M=D
                ,pop D
                @R13
                A=M
                M=D
                ''', thisthat[segment], index)
            else:
                self.store_segment_pointer('R13', segment, index)
                asm(',pop D')
                asm(',set *R13 D')
        else:
            raise SyntaxError('unknown pushPop: %s ; %s ; %s' % (command, segment, index))

    def Close(self):
        self.file.close()

if __name__ == '__main__':
    print('hello')

