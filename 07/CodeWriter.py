from itertools import count

class CodeWriter:
    def __init__(self, output_file):
        self.file = output_file
        self.get_id = count().__next__
        self.symbols = {
                'local'   : 'LCL',
                'argument': 'ARG',
                'this'    : 'THIS',
                'that'    : 'THAT',
                }

    def write(self, s):
        self.file.write(s)
        self.file.write('\n')

    def hlasm(self, s, index=None):
        for line in [l.strip() for l in s.format(index=index).split('\n')]:
            if line == '':
                pass
            elif line[0] == ',':
                # macro
                cmd = line[1:].strip().replace(' ', '_')
                if cmd == '++SP':
                    self.increment_SP()
                elif cmd == '--SP':
                    self.decrement_SP()
                else:
                    getattr(self, cmd)()
            else:
                self.write(line)

    def setFileName(self, fileName):
        pass

    def writeArithmetic(self, command):
        self.write('@10101')
        if command == 'neg':
            self.pop_into_D()         # D = *(SP--);
            self.write('D=-D')
            self.push_from_D()
        elif command == 'not':
            self.pop_into_D()         # D = *(SP--);
            self.write('D=!D')
            self.push_from_D()
        elif command == 'eq':
            self.pop_into_d()         # D = *(SP--);
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
            self.push_from_D()
        elif command == 'gt':
            self.pop_into_D()         # D = *(SP--);
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
            self.push_from_D()
        elif command == 'lt':
            self.pop_into_D()         # D = *(SP--);
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
            self.push_from_D()
        else:
            self.pop_into_D()         # D = *(SP--);

            self.decrement_SP()
            self.write('A=M')         # A = SP

            if   command == 'add': self.write('D=D+M')
            elif command == 'sub': self.write('D=-D\nD=D+M')
            elif command == 'and': self.write('D=D&M')   # D &= *SP
            elif command == 'or' : self.write('D=D|M')   # D |= *SP
            else: self.write('arithmetic: %s' % command)

            self.push_from_D()

    def pop_into_D(self):
        self.decrement_SP()    # SP -= 1
        self.write('A=M')
        self.write('D=M')     # D = *SP

    def push_from_D(self):
        self.set_deref_pointer_to_D('SP')
        self.increment_SP()

    def decrement_SP(self):
        self.write('@SP')
        self.write('M=M-1')       # *SP -= 1
        
    def increment_SP(self):
        self.write('@SP')
        self.write('M=M+1')       # *SP += 1

    def store_segment_pointer(self, dest, segment, index):
        # set A to segment pointer
        self.write('@%s' % self.symbols[segment])

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
        self.write('@10101')
        if command == 'C_PUSH':
            if segment == 'constant':
                self.hlasm('''
                @{index}
                D=A
                ,push from D
                ''', index)
            elif segment == 'temp':
                # push temp index -> onto the stack
                self.hlasm('''
                @R5
                D=A
                @{index}
                D=D+A
                A=D
                D=M
                ,push from D
                ''', index)
            else:
                self.store_segment_pointer('R13', segment, index)
                self.hlasm('''
                @R13
                A=M
                D=M
                ,push from D
                ''')
        elif command == 'C_POP':
            if segment == 'temp':
                self.write('@R5')
                self.write('D=A')
                self.write('@%s' % index)
                self.write('D=D+A')
                self.write('@R13')
                self.write('M=D')
                self.pop_into_D()
                self.write('@R13')
                self.write('A=M')
                self.write('M=D')
            else:
                self.store_segment_pointer('R13', segment, index)
                self.pop_into_D()
                self.set_deref_pointer_to_D('R13')
        else:
            self.write('unknown pushPop: %s ; %s ; %s' % (command, segment, index))

    def Close(self):
        #self.file.close()
        pass

if __name__ == '__main__':
    print('hello')

