#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from clang.cindex import CursorKind as K

dontcare = '^.*$'

if __name__ == '__main__':
    for kind in K.get_all_kinds():
       fmt = '{}: \'{}\''
       msg = fmt.format(kind.name.lower(), dontcare)
       print(msg)
