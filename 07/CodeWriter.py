from itertools import count

class CodeWriter:
    def __init__(self, output_file):
        self.file = output_file
        self.get_id = count().__next__

    def write(self, s):
        self.file.write(s)
        self.file.write('\n')

    def setFileName(self, fileName):
        pass

    def writeArithmetic(self, command):
        if command == 'neg':
            self.pop_into_D()         # D = *(SP--);
            self.write('D=-D')
            self.push_from_D()
        elif command == 'not':
            self.pop_into_D()         # D = *(SP--);
            self.write('D=!D')
            self.push_from_D()
        elif command == 'eq':
            self.pop_into_D()         # D = *(SP--);
            self.decrementSP()        # SP--
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
            self.decrementSP()        # SP--
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
            self.decrementSP()        # SP--
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

            self.decrementSP()
            self.write('A=M')         # A = SP

            if command == 'add':
                self.write('D=D+M')
            elif command == 'sub':
                self.write('D=-D')
                self.write('D=D+M')
            elif command == 'and': self.write('D=D&M')   # D &= *SP
            elif command == 'or': self.write('D=D|M')   # D |= *SP
            else: self.write('arithmetic: %s' % command)

            self.push_from_D()

    def pop_into_D(self):
            self.decrementSP()    # SP -= 1
            self.write('A=M')
            self.write('D=M')     # D = *SP

    def push_from_D(self):
        self.write('@SP')
        self.write('A=M')
        self.write('M=D')
        self.incrementSP()

    def decrementSP(self):
        self.write('@SP')
        self.write('M=M-1')       # *SP -= 1
        
    def incrementSP(self):
        self.write('@SP')
        self.write('M=M+1')       # *SP += 1

    def WritePushPop(self, command, segment, index):
        if command == 'C_PUSH':
            if segment == 'constant':
                self.write('@%s' % index)
                self.write('D=A')
                self.write('@SP')
                self.write('A=M')
                self.write('M=D')
                self.write('D=A+1')
                self.write('@SP')
                self.write('M=D')
            else:
                self.write('unknown segment: %s' % segment)
        elif command == 'C_POP':
            pass
        else:
            self.write('unknown pushPop: %s ; %s ; %s' % (command, segment, index))

    def Close(self):
        #self.file.close()
        pass

if __name__ == '__main__':
    print('hello')

