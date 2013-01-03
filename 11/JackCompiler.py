#! /usr/bin/env python3

import sys

from glob import glob
from argparse import ArgumentParser
from os.path import isdir, join, split, splitext, basename

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

suffix = '.vm'

def get_arguments():
    argument_parser = ArgumentParser(description='Compile Jack code')

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
                    splitext(basename(source))[0] + suffix)
            filenames.append((filename_in, filename_out))
    else:
        filename_in = args.source
        filename_out = join(split(args.source)[0],
                splitext(basename(source))[0] + suffix)
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
        compiler = CompilationEngine(tokenizer, file_out)
        compiler.compileClass()

