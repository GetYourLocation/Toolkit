#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys

try:
    dataset = sys.argv[1]
    data_dir = os.path.join('data', dataset)
except Exception as e:
    print("Usage: python3 %s <directory name>" % sys.argv[0])
    sys.exit(0)

OUTPUT_FILE = 'train.csv'

print("Combining training data...")
files = os.listdir(data_dir)
with open(os.path.join(data_dir, OUTPUT_FILE), 'w') as output_file:
    read_header = True
    for file in files:
        if (file != OUTPUT_FILE):
            with open(os.path.join(data_dir, file), 'r') as data_file:
                lines = data_file.readlines()
            if (read_header):
                output_file.write(lines[0])
                read_header = False
            for line in lines[1:]:
                output_file.write(line)
            print('.', end='')
            sys.stdout.flush()
    print("")
print("Results saved to '%s'." % os.path.join(data_dir, OUTPUT_FILE))
