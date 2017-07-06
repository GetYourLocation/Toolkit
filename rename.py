#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

try:
    author = sys.argv[1]
    cnt = int(sys.argv[2])
except Exception as e:
    print("Usage: python3 %s <author> <start count>" % sys.argv[0])
    sys.exit(0)

files = os.listdir()
for file in files:
    if (file != sys.argv[0]):
        os.rename(file, '%s_%d.jpg' % (author, cnt))
        cnt += 1
