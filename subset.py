#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import time

try:
    ori_dir = os.path.join("data", sys.argv[1])
    res_dir = os.path.join("data", sys.argv[1] + '-subset')
    beg_frame = int(sys.argv[2])
    end_frame = int(sys.argv[3])
    label_name = sys.argv[4]
except Exception as e:
    print("Usage: python3 %s" % sys.argv[0] +
          " <directory name> <begin frame> <end frame> <label>")
    sys.exit(0)

DIR_FRAMES = "JPEGImages"
FILENAME_POS = "pos.csv"
FILENAME_SENSOR = "sensor.csv"
FILENAME_CONFIG = "config.txt"

print("Creating result directory...")
shutil.rmtree(res_dir, ignore_errors=True)
time.sleep(0.2)
os.makedirs(os.path.join(res_dir, DIR_FRAMES))

print("Reading '%s' directory..." % DIR_FRAMES)
frames = os.listdir(os.path.join(ori_dir, DIR_FRAMES))
frames = list(map(lambda filename: int(filename[0:filename.find('.')]),
                  frames))
frames.sort()

print("Reading %s..." % FILENAME_SENSOR)
ori_sensor_file = open(os.path.join(ori_dir, FILENAME_SENSOR), 'r')
ori_sensor_data = ori_sensor_file.readlines()
ori_sensor_file.close()

print("Selecting frames...")
res_sensor_data = [ori_sensor_data[0]]
frame_cnt = 1
i = frames.index(beg_frame)
while i < len(frames):
    if (frames[i] >= beg_frame and frames[i] <= end_frame):
        shutil.copyfile(
            os.path.join(ori_dir, DIR_FRAMES, "%d.jpg" % frames[i]),
            os.path.join(res_dir, DIR_FRAMES, "%d.jpg" % frame_cnt))
        sensor_row = ori_sensor_data[frames[i]]
        sensor_row = str(frame_cnt) + sensor_row[int(sensor_row.find(',')):]
        res_sensor_data.append(sensor_row)
        frame_cnt += 1
    i += 1

print("Selecting sensor data...")
res_sensor_file = open(os.path.join(res_dir, FILENAME_SENSOR), 'w')
for data in res_sensor_data:
    res_sensor_file.write(data)
res_sensor_file.close()

print("Copying %s..." % FILENAME_POS)
shutil.copyfile(os.path.join(ori_dir, FILENAME_POS),
                os.path.join(res_dir, FILENAME_POS))

print("Generating %s..." % FILENAME_CONFIG)
config_file = open(os.path.join(res_dir, FILENAME_CONFIG), 'w')
config_file.write(str(len(res_sensor_data) - 1) + ' ' + label_name)
config_file.close()

print("Results are written to '%s'." % res_dir)
