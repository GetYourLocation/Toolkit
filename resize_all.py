#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from PIL import Image

TARGET_SIZE = (228, 128)
RESIZE_ALG = Image.LANCZOS

try:
    dataset = sys.argv[1]
    data_dir = os.path.join('data', dataset)
    if (len(sys.argv) > 2):
        TARGET_SIZE = (int(sys.argv[2]), int(sys.argv[3]))
except Exception as e:
    print("Usage: python3 %s <directory name>" % sys.argv[0])
    sys.exit(0)

DIR_FRAMES = "JPEGImages"
DATA_TRAIN = "data.csv"
NEW_DATA_TRAIN = "resized_data.csv"

print("Reading training data...")
with open(os.path.join(data_dir, DATA_TRAIN), 'r') as train_file:
    lines = train_file.readlines()

print("Resizing to %d*%d..." % (TARGET_SIZE[0], TARGET_SIZE[1]))
with open(os.path.join(data_dir, NEW_DATA_TRAIN), 'w') as result_file:
    result_file.write(lines[0])
    for line in lines[1:]:
        chunks = line.strip().split(',')
        img_path = os.path.join(data_dir, DIR_FRAMES, chunks[0])
        img = Image.open(img_path)
        w_ratio = TARGET_SIZE[0] / img.width
        h_ratio = TARGET_SIZE[1] / img.height
        img = img.resize(TARGET_SIZE, RESIZE_ALG)
        img.save(img_path, 'JPEG')
        box_idx = 0
        for i, chunk in enumerate(chunks):
            if (i != 0 and chunk != '-'):
                box_idx = i
                break
        box_params = chunks[box_idx].split(' ')
        box_params[0] = float(box_params[0]) * w_ratio
        box_params[1] = float(box_params[1]) * h_ratio
        box_params[2] = float(box_params[2]) * w_ratio
        box_params[3] = float(box_params[3]) * h_ratio
        chunks[box_idx] = "%f %f %f %f" % (box_params[0], box_params[1], box_params[2], box_params[3])
        for i, chunk in enumerate(chunks):
            if (i != 0):
                result_file.write(',')
            result_file.write(chunk)
        result_file.write('\n')
        print('.', end='')
        sys.stdout.flush()
    print("")
print("Done.")
