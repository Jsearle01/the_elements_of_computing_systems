#! /usr/bin/env python3

import functools

from collections import namedtuple

Symbol = namedtuple('Symbol', ['type', 'kind', 'index'])

class SymbolTable():
    def __init__(self, file, debug=False):
        self.symbolDict = {}
        self.debug = debug

        global write
        if debug:
            write = functools.partial(print, file=file)
        else:
            write = lambda x: None

    def startSubroutine(self):
        self.symbolDict = {}

    def Define(self, name, typ, kind):
        index = self.VarCount(kind)
        s = Symbol(typ, kind, index)
        self.symbolDict[name] = s
        write('%s: %s' % (name, s))

    def VarCount(self, kind):
        count = 0
        for name, symbol in self.symbolDict.items():
            if symbol.kind == kind:
                count += 1
        return count

    def Symbol(self, name):
        s = self.symbolDict[name]
        write('%s: %s' % (name, s))
        return s


if __name__ == '__main__':
    print('hello')

