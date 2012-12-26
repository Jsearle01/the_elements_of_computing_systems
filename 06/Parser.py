import re

class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.offset = 0
        self.assembly_code = []
        self.commands = list(self.parseFile())

    def reset(self):
        self.offset = 0

    def hasMoreCommands(self):
        return self.offset < len(self.commands)

    def advance(self):
        self.offset += 1

    def assembly(self):
        return self.assembly_code[self.offset]

    def commandType(self):
        return self.commands[self.offset][0]

    def symbol(self):
        return self.commands[self.offset][1]

    def dest(self):
        return self.commands[self.offset][2]

    def comp(self):
        return self.commands[self.offset][3]

    def jump(self):
        return self.commands[self.offset][4]

    def parseFile(self):
        for line in open(self.filename).readlines():
            # remove comments and whitespace
            line = re.sub(r"//.*", "",line)
            line = re.sub(r"\s", "",line)
            # line = line.strip()
            if line == "":
                continue

            self.assembly_code.append(line)

            if line[0] == "@":
                yield ("A_COMMAND", line[1:])
            elif line[0] == "(":
                yield ("L_COMMAND", line[1:-1])
            else:
                # dest=comp;jump
                eq = line.find("=") >= 0
                sc = line.find(";") >= 0
                if eq and sc:
                    dest, comp, jump = re.split("[=;]", line)
                elif eq:
                    dest, comp = re.split("=", line)
                    jump = "null"
                elif sc:
                    dest = "null"
                    comp, jump = re.split(";", line)
                else:
                    raise SyntaxError

                yield ("C_COMMAND", "", dest, comp, jump)


if __name__ == "__main__":
    p = Parser("add/Add.asm")
    while p.hasMoreCommands():
        print(p.commandType())
        p.advance()

