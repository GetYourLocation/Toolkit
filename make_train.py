#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import shutil
import sys
import urllib.request
import time
import platform


def timestamp():
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


if platform.system() == 'Windows':
    KCF_URL = 'https://github.com/GetYourLocation/KCFcpp/raw/master/bin/KCF.exe'
    KCF_EXEC_PATH = os.path.join('bin', 'KCF.exe')
else:
    KCF_URL = 'https://github.com/GetYourLocation/KCFcpp/raw/master/bin/KCF'
    KCF_EXEC_PATH = os.path.join('bin', 'KCF')

KCF_RESULT_PATH = 'result.txt'
KCF_SHOW_PARAM = ''
IMG_DIR = 'JPEGImages'
TRAIN_LABEL_FILE = 'label.txt'

try:
    dataset = sys.argv[1]
    data_dir = os.path.join("data", dataset)
    data_train_path = "%s_%s.csv" % (dataset, timestamp())
    author = sys.argv[2]
    if (len(sys.argv) > 3 and sys.argv[3] == '-t'):
        KCF_SHOW_PARAM = ' show'
except Exception as e:
    print("Usage: python3 %s <directory name> <author> [-t]" % sys.argv[0])
    sys.exit(0)

# Download KCF executable if not exist
if os.path.exists(KCF_EXEC_PATH):
    print("KCF executable detected at '%s'." % KCF_EXEC_PATH)
else:
    print("Downloading KCF executable...")
    filename, headers = urllib.request.urlretrieve(KCF_URL, KCF_EXEC_PATH)
    print("KCF executable loaded to '%s'." % filename)

print("Building data labels...")
data_headers = ['imageFilename']
with open(TRAIN_LABEL_FILE, 'r') as label_file:
    for line in label_file.readlines():
        data_headers.append(line.strip())

print("Running KCF...")
os.chdir(data_dir)
val = os.system(os.path.join('..', '..', KCF_EXEC_PATH) + KCF_SHOW_PARAM)
if (val != 0 or KCF_SHOW_PARAM != ''):
    sys.exit(val)

print("Writing training data...")
with open(KCF_RESULT_PATH, 'r') as KCF_result_file:
    lines = KCF_result_file.readlines()
with open(data_train_path, 'w') as data_train_file:
    for i, header in enumerate(data_headers):
        if (i > 0):
            data_train_file.write(',')
        data_train_file.write(header)
    data_train_file.write('\n')
    for i, line in enumerate(lines):
        chunks = line.split(' ')

        if (not (chunks[1] in data_headers)):
            print("Invalid label name: %s" % chunks[1])
            sys.exit(1)

        # Rename frame images and write image name
        new_frame_name = '%s_%s_%s' % (author, timestamp(), chunks[0])
        os.rename(os.path.join(IMG_DIR, chunks[0]),
                  os.path.join(IMG_DIR, new_frame_name))
        data_train_file.write(new_frame_name)

        # Write train data
        for header in data_headers[1:]:
            data_train_file.write(',')
            if (chunks[1] == header):
                for i in [2, 3, 4, 5]:
                    if (i != 2):
                        data_train_file.write(' ')
                    data_train_file.write(chunks[i])
            else:
                data_train_file.write('-')
        data_train_file.write('\n')
        print('.', end='')
        sys.stdout.flush()
    print("")
print("Training data saved to '%s'" % os.path.join(data_dir, data_train_path))
