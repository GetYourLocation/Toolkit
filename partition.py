#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import shutil

try:
    partition_cnt = int(sys.argv[1])
except Exception as e:
    print("Usage: python3 %s" % sys.argv[0] +
          " <number of sets in partition>")
    sys.exit(0)

DIR_DATA = "data"
DIR_PARTITION = os.path.join(DIR_DATA, "partition")
DIR_FRAMES = "JPEGImages"

print("Removing directory '%s'..." % DIR_PARTITION, end='')
shutil.rmtree(os.path.join(DIR_PARTITION), ignore_errors=True)
print("Done.")

print("\nCounting frames...")
datasets = os.listdir(DIR_DATA)
frame_tot = 0
for i, dataset in enumerate(datasets):
    path = os.path.join(DIR_DATA, dataset, DIR_FRAMES)
    frame_cnt = len(os.listdir(path))
    if frame_cnt > 0:
        datasets[i] = (datasets[i], frame_cnt)
        frame_tot += frame_cnt
datasets = sorted(datasets, key=lambda x: x[1], reverse=True)
frame_partition = frame_tot // partition_cnt
print("Total frames: %d" % frame_tot)
print("Expect average: %d" % frame_partition)

print("\nGenerating partition plan...")
mv_seq, remain_data = [], []
frame_cnt = [0] * partition_cnt
# First fit
for dataset in datasets:
    i = 0
    while (i < partition_cnt):
        frame_cnt_next = frame_cnt[i] + dataset[1]
        if (frame_cnt_next < frame_partition):
            src = os.path.join(DIR_DATA, dataset[0])
            des = os.path.join(DIR_PARTITION, str(i + 1), dataset[0])
            mv_seq.append((src, des))
            frame_cnt[i] = frame_cnt_next
            break
        i += 1
    if (i == partition_cnt):
        remain_data.append(dataset)
# Assign remain datasets to partition with the minimum frames
for dataset in remain_data:
    min_partition = frame_cnt.index(min(frame_cnt))
    src = os.path.join(DIR_DATA, dataset[0])
    des = os.path.join(DIR_PARTITION, str(min_partition + 1), dataset[0])
    mv_seq.append((src, des))
    frame_cnt[min_partition] += dataset[1]
for i in range(partition_cnt):
    print("Partition #%d: %d frames" % (i + 1, frame_cnt[i]))
print("Done.")

key = input("\nPRESS ENTER TO PARTITION ")
if (len(key) != 0):
    print("Bye.")
else:
    for i in range(partition_cnt):
        os.makedirs(os.path.join(DIR_PARTITION, str(i + 1)))
    for seq in mv_seq:
        shutil.move(seq[0], seq[1])
    # Check parition validity
    cnt = 0
    for i in range(partition_cnt):
        path_partition = os.path.join(DIR_PARTITION, str(i + 1))
        for data_dir in os.listdir(path_partition):
            frame_dir = os.path.join(path_partition, data_dir, DIR_FRAMES)
            cnt += len(os.listdir(frame_dir))
    if cnt == frame_tot:
        print("Results are saved to '%s'." % DIR_PARTITION)
    else:
        print("Bad partition.")
