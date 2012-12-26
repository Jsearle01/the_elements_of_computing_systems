#! /usr/bin/env python3

from Parser import Parser
from Code import dest, comp, jump
from SymbolTable import SymbolTable

from os.path import basename, splitext
from argparse import ArgumentParser
from sys import stdout

import itertools

arg_parser = ArgumentParser(description='Hack Assembler')

arg_parser.add_argument('filename',
        default='main.asm',
        help='a file to assemble')

arg_parser.add_argument('--verbose',
        dest='verbose',
        action='store_true',
        help='set output to verbose')

arg_parser.add_argument('--out',
        dest='output_filename',
        default='',
        help='set output file')

args = arg_parser.parse_args()

p = Parser(args.filename)

offset = 0
symbols = SymbolTable()

while p.hasMoreCommands():
    t = p.commandType()
    if t == 'A_COMMAND':
        offset += 1
        s = p.symbol()
    elif t == 'C_COMMAND':
        offset += 1
    elif t == 'L_COMMAND':
        s = p.symbol()
        if symbols.contains(s):
            raise SyntaxError("multiple declarations of %s" % s)
        else:
            symbols.addEntry(s, offset)
    else:
        raise Error
    p.advance()

p.reset()
output = []
variable_offset = itertools.count(16)

def new_variable(name):
    symbols.addEntry(name, variable_offset.__next__())

while p.hasMoreCommands():
    t = p.commandType()
    if t == 'A_COMMAND':
        s = p.symbol()
        try:
            a = int(s)
        except ValueError:
            if not symbols.contains(s):
                new_variable(s)
            a = symbols.GetAddress(p.symbol())
        byte = '0{:015b}'.format(a)
    elif t == 'C_COMMAND':
        byte = '111{}{}{}'.format(
                comp(p.comp()),
                dest(p.dest()),
                jump(p.jump()))
        pass
    elif t == 'L_COMMAND':
        byte = ''
        pass # handled in first pass
    else:
        raise Error
    output.append((byte, p.assembly()))
    p.advance()

if args.output_filename == '':
    args.output_filename = splitext(args.filename)[0] + '.hack'

if args.output_filename == '-':
    f = stdout
else:
    f = open(args.output_filename, "w")

for machine_code, assembly in output:
    if args.verbose:
        f.write('{:16} - {}'.format(machine_code, assembly))
        f.write("\n")
    else:
        if machine_code != '':
            f.write(machine_code)
            f.write("\n")

