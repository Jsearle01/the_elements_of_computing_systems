#! /usr/bin/env python3

import collections
import re
import html
import sys
import functools

from argparse import ArgumentParser
from os.path import split, splitext, isdir, join, basename

Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])

keywords = '''
        class constructor function
        method field static var
        int char boolean void true
        false null this let do
        if else while return
        '''.split()

symbols = '''
        { } ( ) [ ] .
        , ; + - * / &
        | < > = ~
        '''.split()

re_symbols = '[{}]'.format(re.escape(''.join(symbols)))

def isKeyword(word):
    return word in keywords

def isSymbol(c):
    return c in symbols

class JackTokenizer():
    def __init__(self, file):
        self.currentToken = 0
        self.tokens = tuple(self.tokenize(file.read()))
        self.tokensLength = len(self.tokens)

    def hasMoreTokens(self):
        return self.currentToken < self.tokensLength

    def advance(self):
        self.currentToken += 1

    def token(self):
        return self.tokens[self.currentToken]

    def tokenType(self):
        return self.tokens[self.currentToken].typ

    def tokenValue(self):
        return self.tokens[self.currentToken].val

    def tokenize(self, s):
        'taken from python re module documentation'
        token_specification = [
            ('integerConstant',  r'\d+'),           # Integer
            ('identifier',      r'[A-Za-z0-9_]+'), # Identifiers
            # ('symbol',  r'[{}()\[\].,;+\-*\/&|<>=~]'),      # Symbols
            ('symbol',  re_symbols),      # Symbols
            ('stringConstant', r'"(\.|[^"])*"'),   # Line endings
            ('newline', r'\n'),            # Line endings
            ('skip',    r'[ \t]'),         # Skip over spaces and tabs
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex).match
        line = 1
        pos = line_start = 0
        mo = get_token(s)
        while mo is not None:
            typ = mo.lastgroup
            if typ == 'newline':
                line_start = pos
                line += 1
            elif typ != 'skip':
                val = mo.group(typ)
                if typ == 'identifier' and val in keywords:
                    typ = 'keyword'
                elif typ == 'stringConstant':
                    # strip quotes
                    val = val[1:-1]
                yield Token(typ, val, line, mo.start()-line_start)
            pos = mo.end()
            mo = get_token(s, pos)
        if pos != len(s):
            raise RuntimeError('Unexpected character %r on line %d' %(s[pos], line))


def get_arguments():
    argument_parser = ArgumentParser(description='tokenize Jack code')

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
        filename_out = splitext(basename(args.source))[0] + 'T.xml'
        filenames = [(filename_in, filename_out)]
    return filenames

if __name__ == '__main__':
    args = get_arguments()

    filenames = get_filenames(args.source)

    for filename_in, filename_out in filenames:
        if args.stdout:
            write = print
        else:
            write = functools.partial(print,
                    file= open(filename_out, "w"))

        try:
            j = JackTokenizer(open(filename_in))

            write('<tokens>')
            while j.hasMoreTokens():
                typ, val, _, _ = j.token()
                val = html.escape(val)
                write('<{}> {} <{}>'.format(typ, val, typ))
                j.advance()
            write('</tokens>')
        except RuntimeError as s:
            print(s)

