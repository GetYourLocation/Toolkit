#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

try:
    frame_dir = os.path.join('data', sys.argv[1], 'JPEGImages')
except Exception as e:
    print("Usage: python3 norm.py <directory name>")
    sys.exit(0)

frame_files = os.listdir(frame_dir)
for frame_name in frame_files:
    chunks = frame_name.split('.')
    frame_cnt = int(chunks[0])
    ext = chunks[1]
    os.rename(os.path.join(frame_dir, frame_name),
              os.path.join(frame_dir, str(frame_cnt) + '.' + ext))
print("Done.")
