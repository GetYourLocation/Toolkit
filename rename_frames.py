#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

try:
    root_dir = sys.argv[1]
except Exception as e:
    print("Usage: python3 rename_frames.py <directory name>")
    sys.exit(0)

ori_name = 'frames'
new_name = 'JPEGImages'

os.chdir(root_dir)
dirs = os.listdir()
for dir_ in dirs:
    try:
        os.rename(os.path.join(dir_, ori_name), os.path.join(dir_, new_name))
    except Exception as e:
        pass
