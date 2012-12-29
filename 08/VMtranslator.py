#! /usr/bin/env python3

from VMParser import VMParser
from CodeWriter import CodeWriter

from os.path import splitext, isdir, join
from argparse import ArgumentParser
from glob import glob

import sys

argument_parser = ArgumentParser(description='translate Hack vm to Hack asm')

argument_parser.add_argument(
    'source',
    metavar='source',
    help=''
    )

argument_parser.add_argument('--stdout',
        dest='stdout',
        action='store_true',
        help='print to stdout')

args = argument_parser.parse_args()

output_filename = splitext(args.source)[0] + '.asm'

if args.stdout:
    output_file = sys.stdout
else:
    output_file = open(output_filename, "w")

cw = CodeWriter(output_file)

if isdir(args.source):
    filenames = glob(join(args.source, '*.vm'))
else:
    filenames = [args.source]

cw.writeInit()

for filename in filenames:
    cw.setFileName(filename)
    p = VMParser(filename)
    while p.hasMoreCommands():
        t = p.commandType()
        if t in ['C_PUSH', 'C_POP']:
            cw.WritePushPop(t, p.arg1(), p.arg2())
        elif t == 'C_ARITHMETIC':
            cw.writeArithmetic(p.arg1())
        elif t == 'C_LABEL':
            cw.writeLabel(p.arg1())
        elif t == 'C_GOTO':
            cw.writeGoto(p.arg1())
        elif t == 'C_IF':
            cw.writeIf(p.arg1())
        elif t == 'C_FUNCTION':
            cw.writeFunction(p.arg1(), p.arg2())
        elif t == 'C_RETURN':
            cw.writeReturn()
        else:
            raise SyntaxError('unknown command: %s ; %s' % (t, p.commands[p.offset]))
        p.advance()

cw.Close()

