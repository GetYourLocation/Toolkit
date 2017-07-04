#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from PIL import Image
import os
import sys

TARGET_SIZE = (228, 128)
RESIZE_ALG = Image.LANCZOS

try:
    dataset = sys.argv[1]
    data_dir = os.path.join('data', dataset)
    if (len(sys.argv) > 2):
        TARGET_SIZE = (int(sys.argv[2]), int(sys.argv[3]))
except Exception as e:
    print("Usage: python3 %s <directory name> [<target width> <target height>]" % sys.argv[0])
    sys.exit(0)

DIR_FRAMES = "JPEGImages"

print("Resizing to %d*%d..." % (TARGET_SIZE[0], TARGET_SIZE[1]))
img_dir = os.path.join(data_dir, DIR_FRAMES)
for img_name in os.listdir(img_dir):
    img_path = os.path.join(img_dir, img_name)
    img = Image.open(img_path)
    img = img.resize(TARGET_SIZE, RESIZE_ALG)
    img.save(img_path, 'JPEG')
    print('.', end='')
    sys.stdout.flush()
print("")
print("Done.")
