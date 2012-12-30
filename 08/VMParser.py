
import re

commandTypes = {
        'add'     : 'C_ARITHMETIC',
        'sub'     : 'C_ARITHMETIC',
        'neg'     : 'C_ARITHMETIC',
        'eq'      : 'C_ARITHMETIC',
        'gt'      : 'C_ARITHMETIC',
        'lt'      : 'C_ARITHMETIC',
        'and'     : 'C_ARITHMETIC',
        'or'      : 'C_ARITHMETIC',
        'not'     : 'C_ARITHMETIC',
        'push'    : 'C_PUSH',
        'pop'     : 'C_POP',
        'label'   : 'C_LABEL',
        'goto'    : 'C_GOTO',
        'if-goto' : 'C_IF',
        'function': 'C_FUNCTION',
        'return'  : 'C_RETURN',
        'call'    : 'C_CALL',
        'breakpoint'    : 'C_BREAKPOINT'
        }

class VMParser:
    def __init__(self, filename):
        self.commands = []
        self.offset = 0
        line_number = -1

        f = open(filename)
        for line in f.readlines():
            line_number += 1
            line = re.sub(r"//.*", "",line)
            line = line.strip()
            if line == '': continue
            self.parseLine(line, line_number)
        f.close()

    def parseLine(self, line, line_number):
        self.commands.append(line.split())

    def hasMoreCommands(self):
        return self.offset < len(self.commands)

    def advance(self):
        self.offset += 1

    def commandType(self):
        return commandTypes[self.commands[self.offset][0]]

    def arg1(self):
        if self.commandType() == 'C_ARITHMETIC':
            return self.commands[self.offset][0]
        else:
            return self.commands[self.offset][1]

    def arg2(self):
        return self.commands[self.offset][2]

if __name__ == '__main__':
    p = VMParser('StackArithmetic/SimpleAdd/SimpleAdd.vm')
    while p.hasMoreCommands():
        print(p.commands[p.offset])
        p.advance()

