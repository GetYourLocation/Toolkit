#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import random

try:
    dataset = sys.argv[1]
    data_dir = os.path.join('data', dataset)
except Exception as e:
    print("Usage: python3 %s <directory name>" % sys.argv[0])
    sys.exit(0)

IMG_DIR = 'JPEGImages'
OUTPUT_FILE = 'train.csv'

print("Collecting training data...")
dataLines = []
header = ''
files = os.listdir(data_dir)
read_header = True
for file in files:
    if (not (file in [OUTPUT_FILE, IMG_DIR])):
        with open(os.path.join(data_dir, file), 'r') as data_file:
            lines = data_file.readlines()
        if (read_header):
            header = lines[0]
            read_header = False
        for line in lines[1:]:
            img_name = line.strip().split(',')[0]
            img_path = os.path.join(data_dir, IMG_DIR, img_name)
            if (not os.path.isfile(img_path)):
                print("Error: '%s' not found." % img_path)
                sys.exit(1)
            dataLines.append(line)
        print('.', end='')
        sys.stdout.flush()
print("")

print("Writing results...")
random.shuffle(dataLines)
with open(os.path.join(data_dir, OUTPUT_FILE), 'w') as output_file:
    output_file.write(header)
    for line in dataLines:
        output_file.write(line)
print("Results saved to '%s'." % os.path.join(data_dir, OUTPUT_FILE))
