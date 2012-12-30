#! /usr/bin/env python3

import fileinput
import collections

def strip(s): return s.strip()
def stamp(s): return s.find('@1230') == 0

stamps = {
        '@12300' : 'init',
        '@12301' : 'label',
        '@12302' : 'goto',
        '@12303' : 'if',
        '@12304' : 'call',
        '@12305' : 'function',
        '@12306' : 'return',
        '@12307' : 'arithmetic',
        '@12308' : 'push',
        '@12309' : 'pop',
        }

c = collections.Counter(filter(stamp, map(strip, fileinput.input())))

for line, count in c.most_common(5):
    print('%4d - %s - %s' % (count, line, stamps[line]))

