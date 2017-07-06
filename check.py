#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings("ignore")

try:
    dataset = sys.argv[1]
    data_dir = os.path.join('data', dataset)
except Exception as e:
    print("Usage: python3 %s <directory name>" % sys.argv[0])
    sys.exit(0)

DATA_FILE_PATH = os.path.join(data_dir, 'data.csv')
IMG_DIR = os.path.join(data_dir, 'JPEGImages')

ax = plt.gca()

with open(DATA_FILE_PATH, 'r') as data_file:
    lines = data_file.readlines()
headers = lines[0].strip().split(',')
for line in lines[1:]:
    chunks = line.strip().split(',')
    label_name = ''
    bbox_str = ''
    for i, chunk in enumerate(chunks):
        if (i != 0 and chunk != '-'):
            label_name = headers[i]
            bbox_str = chunk
            bbox_strs = chunk.split(' ')
            x1 = float(bbox_strs[0])
            y1 = float(bbox_strs[1])
            width = float(bbox_strs[2]) - x1
            height = float(bbox_strs[3]) - y1
            break
    print("[%s] [%s] [%s]" % (chunks[0], label_name, bbox_str), end='')
    sys.stdout.flush()
    img = plt.imread(os.path.join(IMG_DIR, chunks[0]))
    plt.imshow(img)
    rect = Rectangle((x1, y1), width, height)
    rect.set_edgecolor('yellow')
    rect.set_facecolor('none')
    ax.add_patch(rect)
    plt.pause(0.001)
    input("")
    rect.remove()
