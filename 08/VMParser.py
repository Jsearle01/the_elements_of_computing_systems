
import re

commandTypes = {
        'add'       : 'C_ARITHMETIC',
        'sub'       : 'C_ARITHMETIC',
        'neg'       : 'C_ARITHMETIC',
        'eq'        : 'C_ARITHMETIC',
        'gt'        : 'C_ARITHMETIC',
        'lt'        : 'C_ARITHMETIC',
        'and'       : 'C_ARITHMETIC',
        'or'        : 'C_ARITHMETIC',
        'not'       : 'C_ARITHMETIC',
        'push'      : 'C_PUSH',
        'pop'       : 'C_POP',
        'label'     : 'C_LABEL',
        'goto'      : 'C_GOTO',
        'if-goto'   : 'C_IF',
        'function'  : 'C_FUNCTION',
        'return'    : 'C_RETURN',
        'call'      : 'C_CALL',
        'breakpoint': 'C_BREAKPOINT',
        'hlasm'     : 'C_HLASM'
        }

def read_till(f, end_marker):
    lines = []
    while True:
        line = f.readline()
        if line == '':
            raise SyntaxError('reached EOF while parsing hlasm command')
        line = line.strip()
        if line == end_marker:
            return lines
        else:
            lines.append(line)

class VMParser:
    def __init__(self, filename):
        self.commands = []
        self.offset = 0
        parsing = True
        f = open(filename)
        while parsing:
            parsing = self.parseLine(f)
        f.close()

    def parseLine(self, f):
        line = f.readline()
        if line == '':
            return False

        line = re.sub(r"//.*", "",line)
        line = line.strip()
        if line == '':
            return True

        words = line.split()
        if words[0] == 'hlasm':
            end_marker = words[1]
            code = read_till(f, words[1])
            self.commands.append((words[0], '\n'.join(code)))
        else:
            self.commands.append(words)
        return True

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

