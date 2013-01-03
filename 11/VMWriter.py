#! /usr/bin/env python3

class VMWriter():
    def __init__(self, file):
        self.file = file

    def writePush(self, segment, index):
        pass

    def writePop(self, Segment, index):
        pass

    def WriteArithmetic(self, command):
        pass

    def WriteLabel(self, label):
        pass

    def WriteGoto(self, label):
        pass

    def WriteIf(self, label):
        pass

    def writeCall(self, name, nArgs):
        pass

    def writeReturn(self):
        pass


if __name__ == '__main__':
    print('hello')

