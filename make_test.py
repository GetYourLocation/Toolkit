#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random

try:
    dataset = sys.argv[1]
    test_samples = int(sys.argv[2])
    data_dir = os.path.join("data", dataset)
except Exception as e:
    print("Usage: python3 %s <directory name> <test samples for each label>" % sys.argv[0])
    sys.exit(0)

train_path = os.path.join(data_dir, 'train.csv')
new_train_path = os.path.join(data_dir, 'new_train.csv')
new_test_path = os.path.join(data_dir, 'new_test.csv')

print("Reading training data....")
with open(train_path, 'r') as file:
    lines = file.readlines()

print("Collecting data for each label...")
d = {}
for line in lines[1:]:
    chunks = line.split(',')
    for i, chunk in enumerate(chunks[1:]):
        if (chunk.find('-') == -1):
            if (i in d):
                d[i].append(chunks[0])
            else:
                d[i] = []
            break

print("Selecting data...")
test_files = []
for key in d:
    test_files += random.sample(d[key], test_samples)

print("Writing results...")
with open(new_train_path, 'w') as new_train_file:
    new_train_file.write(lines[0])
    with open(new_test_path, 'w') as new_test_file:
        new_test_file.write(lines[0])
        for line in lines[1:]:
            chunks = line.split(',')
            if (chunks[0] in test_files):
                new_test_file.write(line)
            else:
                new_train_file.write(line)
print("Done.")
