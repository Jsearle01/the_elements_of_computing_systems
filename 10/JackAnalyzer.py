#! /usr/bin/env python3

import sys

from argparse import ArgumentParser
from os.path import isdir, join, split, splitext, basename

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

def get_arguments():
    argument_parser = ArgumentParser(description='Analyze Jack code')

    argument_parser.add_argument(
        'source',
        metavar='source',
        help=''
        )

    argument_parser.add_argument('--stdout',
        dest='stdout',
        action='store_true',
        help='print to stdout')

    return argument_parser.parse_args()

def get_filenames(source):
    if isdir(source):
        filenames = []
        source = args.source.rstrip('/')
        for filename_in in glob(join(source, '*.jack')):
            filename_out = join(source,
                    splitext(basename(source))[0] + 'T.xml')
            filenames.append((filename_in, filename_out))
    else:
        filename_in = args.source
        filename_out = join(split(args.source)[0],
                splitext(basename(source))[0] + 'T.xml')
        filenames = [(filename_in, filename_out)]
    return filenames


if __name__ == '__main__':
    args = get_arguments()

    filenames = get_filenames(args.source)

    for filename_in, filename_out in filenames:
        if args.stdout:
            file_out = sys.stdout
        else:
            file_out = open(filename_out, "w")

        tokenizer = JackTokenizer(open(filename_in))
        compiler = CompilationEngine(tokenizer, filename_out)
        compiler.compileClass()

