#! /usr/bin/env python3

import functools

class VMWriter():
    def __init__(self, file):
        global write
        write = functools.partial(print, file=file)


    def writePush(self, segment, index):
        write('push {} {}'.format(segment, index))

    def writePop(self, segment, index):
        write('pop {} {}'.format(segment, index))

    def WriteArithmetic(self, command):
        write('{}'.format(command))

    def WriteLabel(self, label):
        write('label {}'.format(label))

    def WriteGoto(self, label):
        write('goto {}'.format(label))

    def WriteIf(self, label):
        write('if-goto {}'.format(label))

    def writeCall(self, name, nArgs):
        write('call {} {}'.format(name, nArgs))
        if nArgs == 0:
            self.writePop('temp', 0)

    def writeFunction(self, name, nLocals):
        write('function {} {}'.format(name, nLocals))

    def writeReturn(self):
        write('return'.format())


if __name__ == '__main__':
    print('hello')

