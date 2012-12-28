from itertools import count
from functools import partial

import os.path

thisthat = {
        '0': 'THIS',
        '1': 'THAT',
        'this': 'THIS',
        'that': 'THAT',
        }

symbols = {
        'local'   : 'LCL',
        'argument': 'ARG',
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

    def hlasm(self, s, *args):
        lines = [l.strip() for l in s.format(*args).split('\n')]
        aliases = {
                '++SP': self.increment_SP,
                '--SP': self.decrement_SP,
                }

        for line in lines:
            if line == '':
                pass
            elif line[0] == ',':
                # macro
                cmd, *args = line[1:].strip().split()
                if cmd in aliases:
                    aliases[cmd](*args)
                else:
                    getattr(self, 'macro_' + cmd)(*args)
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
        ''')

    def writeReturn(self):
        asm('''
        ,stamp 5
        ''')

    def writeFunction(self, functionName, numLocals):
        asm('''
        ,stamp 6
        ''')

    def writeArithmetic(self, command):
        asm('''
        ,stamp 7
        ''')
        if command == 'neg':
            self.pop_D()         # D = *(SP--);
            self.write('D=-D')
            self.push_D()
        elif command == 'not':
            self.pop_D()         # D = *(SP--);
            self.write('D=!D')
            self.push_D()
        elif command == 'eq':
            self.pop_D()         # D = *(SP--);
            self.decrement_SP()       # SP--
            self.write('A=M')         # A = SP

            self.write('D=D-M')       # D -= *SP

            symbol_id = self.get_id()

            self.write('@EQ_TRUE_%s' % symbol_id)
            self.write('D;JEQ')
            self.write('D=0')
            self.write('@EQ_END_%s' % symbol_id)
            self.write('0;JMP')
            self.write('(EQ_TRUE_%s)' % symbol_id)
            self.write('D=-1')
            self.write('(EQ_END_%s)' % symbol_id)
            self.push_D()
        elif command == 'gt':
            self.pop_D()         # D = *(SP--);
            self.decrement_SP()        # SP--
            self.write('A=M')         # A = SP

            self.write('D=D-M')       # D -= *SP

            symbol_id = self.get_id()

            self.write('@GT_TRUE_%s' % symbol_id)
            self.write('D;JLT')
            self.write('D=0')
            self.write('@GT_END_%s' % symbol_id)
            self.write('0;JMP')
            self.write('(GT_TRUE_%s)' % symbol_id)
            self.write('D=-1')
            self.write('(GT_END_%s)' % symbol_id)
            self.push_D()
        elif command == 'lt':
            self.pop_D()         # D = *(SP--);
            self.decrement_SP()        # SP--
            self.write('A=M')         # A = SP

            self.write('D=D-M')       # D -= *SP

            symbol_id = self.get_id()

            self.write('@LT_TRUE_%s' % symbol_id)
            self.write('D;JGT')
            self.write('D=0')
            self.write('@LT_END_%s' % symbol_id)
            self.write('0;JMP')
            self.write('(LT_TRUE_%s)' % symbol_id)
            self.write('D=-1')
            self.write('(LT_END_%s)' % symbol_id)
            self.push_D()
        else:
            asm('''
            ,pop D
            ,--SP
            A=M
            ''')

            if   command == 'add': self.write('D=D+M')
            elif command == 'sub': self.write('D=-D\nD=D+M')
            elif command == 'and': self.write('D=D&M')   # D &= *SP
            elif command == 'or' : self.write('D=D|M')   # D |= *SP
            else: self.write('arithmetic: %s' % command)

            asm(',push D')

    def macro_pop(self, dest):
        if dest == 'D':
            asm('''
            ,--SP
            A=M
            D=M
            ''')
        else:
            raise Error('unknown pop destination')

    def macro_push(self, dest):
        if dest == 'D':
            self.set_deref_pointer_to_D('SP')
            self.increment_SP()
        else:
            raise Error('unknown push destination')

    def macro_stamp(self, id_number):
        asm('''
        @{0}
        @{1}
        ''', 12345, 12300 + int(id_number))
    def decrement_SP(self):
        asm('''
        @SP
        M=M-1
        ''')
        
    def increment_SP(self):
        asm('''
        @SP
        M=M+1
        ''')

    def store_segment_pointer(self, dest, segment, index):
        # set A to segment pointer
        self.write('@%s' % symbols[segment])

        # increment pointer by index
        self.write('D=M')
        self.write('@%s' % index)
        self.write('D=D+A')

        # store pointer
        self.write('@%s' % dest)
        self.write('M=D')
            
    def set_deref_pointer_to_D(self, dest) :
        self.write('@%s' % dest)
        self.write('A=M')
        self.write('M=D')

    def set_memory_to_D(self, dest):
        self.write('@%s' % dest)
        self.write('M=D')

    def WritePushPop(self, command, segment, index):
        asm('''
        ,stamp 8
        ''')
        if command == 'C_PUSH':
            if segment == 'constant':
                self.hlasm('''
                @{0}
                D=A
                ,push D
                ''', index)
            elif segment == 'static':
                self.write('@%s.%s' % (self.filename, index))
                self.hlasm('''
                D=M
                ,push D
                ''')
            elif segment == 'temp':
                # push temp index -> onto the stack
                self.hlasm('''
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
                self.write('@R5')
                self.write('D=A')
                self.write('@%s' % index)
                self.write('D=D+A')
                self.write('@R13')
                self.write('M=D')
                self.pop_D()
                self.write('@R13')
                self.write('A=M')
                self.write('M=D')
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
                self.set_deref_pointer_to_D('R13')
        else:
            raise SyntaxError('unknown pushPop: %s ; %s ; %s' % (command, segment, index))

    def Close(self):
        #self.file.close()
        pass

if __name__ == '__main__':
    print('hello')

