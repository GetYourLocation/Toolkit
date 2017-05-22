#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
import os
import shutil
import sys
import urllib.request
import cv2
import time

KCF_URL = 'https://github.com/GetYourLocation/KCFcpp/raw/master/bin/KCF'
KCF_EXEC_PATH = os.path.join('bin', 'KCF')
KCF_RESULT_PATH = 'result.txt'
KCF_SHOW_PARAM = ''
XML_DIR = 'Annotations'
IMG_DIR = 'JPEGImages'

try:
    dataset = sys.argv[1]
    data_dir = os.path.join("data", dataset)
    author = sys.argv[2]
    if (len(sys.argv) > 3 and sys.argv[3] == '-s'):
        KCF_SHOW_PARAM = ' show'
except Exception as e:
    print("Usage: python3 make_train.py <directory name> <author> [-s]")
    sys.exit(0)


def timestamp():
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


# Download KCF executable if not exist
if os.path.exists(KCF_EXEC_PATH):
    print("KCF executable detected at '%s'." % KCF_EXEC_PATH)
else:
    print("Downloading KCF executable...")
    filename, headers = urllib.request.urlretrieve(KCF_URL, KCF_EXEC_PATH)
    print("KCF executable loaded to '%s'." % filename)

print("Running KCF...")
os.chdir(data_dir)
val = os.system(os.path.join('..', '..', KCF_EXEC_PATH) + KCF_SHOW_PARAM)
if val != 0:
    sys.exit(0)

print("Generating XML...")
with open(KCF_RESULT_PATH, 'r') as resultFile:
    lines = resultFile.readlines()
shutil.rmtree(XML_DIR, ignore_errors=True)
os.mkdir(XML_DIR)
for i, line in enumerate(lines):
    print('.', end='')
    sys.stdout.flush()

    chunks = line.split(' ')

    # Read frame images
    frame_img = cv2.imread(os.path.join(IMG_DIR, chunks[0]))
    img_height, img_width, img_depth = frame_img.shape

    # Rename frame images
    new_frame_name = '%s_%s_%s' % (author, timestamp(), chunks[0])
    os.rename(os.path.join(IMG_DIR, chunks[0]),
              os.path.join(IMG_DIR, new_frame_name))

    # Create XML document
    root = Element('annotation')

    folder = SubElement(root, 'folder')
    folder.text = dataset
    filename = SubElement(root, 'filename')
    filename.text = new_frame_name

    source = SubElement(root, 'source')
    source_database = SubElement(source, 'database')
    source_database.text = 'GYL Database'
    source_annotation = SubElement(source, 'annotation')
    source_annotation.text = 'GYL'
    source_image = SubElement(source, 'image')
    source_image.text = 'flickr'
    source_flickrid = SubElement(source, 'flickrid')
    source_flickrid.text = 'NULL'

    owner = SubElement(root, 'owner')
    owner_flickrid = SubElement(owner, 'flickrid')
    owner_flickrid.text = 'NULL'
    owner_name = SubElement(owner, 'name')
    owner_name.text = 'GYL'

    size = SubElement(root, 'size')
    size_width = SubElement(size, 'width')
    size_width.text = str(img_width)
    size_height = SubElement(size, 'height')
    size_height.text = str(img_height)
    size_depth = SubElement(size, 'depth')
    size_depth.text = str(img_depth)

    segmented = SubElement(root, 'segmented')
    segmented.text = '0'

    object_ = SubElement(root, 'object')
    object_name = SubElement(object_, 'name')
    object_name.text = chunks[1]
    object_pose = SubElement(object_, 'pose')
    object_pose.text = 'Unspecified'
    object_truncated = SubElement(object_, 'truncated')
    object_truncated.text = '0'
    object_difficult = SubElement(object_, 'difficult')
    object_difficult.text = '0'

    object_bndbox = SubElement(object_, 'bndbox')
    object_bndbox_xmin = SubElement(object_bndbox, 'xmin')
    object_bndbox_xmin.text = chunks[2]
    object_bndbox_ymin = SubElement(object_bndbox, 'ymin')
    object_bndbox_ymin.text = chunks[3]
    object_bndbox_xmax = SubElement(object_bndbox, 'xmax')
    object_bndbox_xmax.text = chunks[4]
    object_bndbox_ymax = SubElement(object_bndbox, 'ymax')
    object_bndbox_ymax.text = chunks[5]

    # Write XML document to file
    reparsed = minidom.parseString(ElementTree.tostring(root))
    xml_str = reparsed.toprettyxml(indent='\t')
    xml_str = xml_str[xml_str.index('\n') + 1:]
    xml_path = os.path.join(XML_DIR, new_frame_name.split('.')[0] + '.xml')
    with open(xml_path, 'w') as xml_file:
        xml_file.write(xml_str)
print("XMLs are saved to directory 'Annotations'.")
