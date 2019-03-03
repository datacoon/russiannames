# -*- coding: UTF-8 -*-

import sys
from russiannames.parser import NamesParser
from pprint import pprint

if __name__ == '__main__':
    import locale
    np = NamesParser()
    pprint(np.parse(sys.argv[1]))
