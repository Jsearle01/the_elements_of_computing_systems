#! /usr/bin/env python3

import re
from sys import argv

a = open(argv[1]).read()

print(re.sub(r'^D=(.*)\n(.*)=D$', r'\2=\1', a, flags=re.MULTILINE))

