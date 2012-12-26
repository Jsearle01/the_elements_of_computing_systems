#! /usr/bin/env python3

from Parser import Parser
from Code import dest, comp, jump

from os.path import basename, splitext
from argparse import ArgumentParser
from sys import stdout

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

output = []

while p.hasMoreCommands():
    t = p.commandType()
    if t == 'A_COMMAND':
        a = int(p.symbol())
        byte = '0{:015b}'.format(a)
    elif t == 'C_COMMAND':
        byte = '111{}{}{}'.format(
                comp(p.comp()),
                dest(p.dest()),
                jump(p.jump()))
        pass
    elif t == 'L_COMMAND':
        byte = ('l', p.symbol())
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
        f.write('%s - %s' % (machine_code, assembly))
    else:
        f.write(machine_code)
    f.write("\n")

