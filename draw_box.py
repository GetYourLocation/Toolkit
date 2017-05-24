#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import xml.dom.minidom
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

try:
    dataset = sys.argv[1]
    data_dir = os.path.join('data', dataset)
except Exception as e:
    print("Usage: python3 %s <directory name>" % sys.argv[0])
    sys.exit(0)

xml_dir = os.path.join(data_dir, 'Annotations')
img_dir = os.path.join(data_dir, 'JPEGImages')

xml_cnt = 1
xml_filenames = os.listdir(xml_dir)

for xml_filename in xml_filenames:
    xml_path = os.path.join(xml_dir, xml_filename)
    root = xml.dom.minidom.parse(xml_path).documentElement

    # Read size from XML
    root_size = root.getElementsByTagName("size")[0]
    root_size_w = int(root_size.getElementsByTagName("width")[0]
                      .childNodes[0].data)
    root_size_h = int(root_size.getElementsByTagName("height")[0]
                      .childNodes[0].data)
    root_size_d = int(root_size.getElementsByTagName("depth")[0]
                      .childNodes[0].data)

    # Read image
    root_filename = root.getElementsByTagName("filename")[0].childNodes[0].data
    img = plt.imread(os.path.join(img_dir, root_filename))

    # Check image size
    assert img.shape == (root_size_h, root_size_w, root_size_d)

    # Show image
    ax = plt.gca()
    plt.imshow(img)

    # Draw rectangule
    objs = root.getElementsByTagName("object")
    for obj in objs:
        obj_name = obj.getElementsByTagName("name")[0].childNodes[0].data
        print("(%04d) (obj_name: %s) %s"
              % (xml_cnt, obj_name, xml_filename), end='')
        xml_cnt += 1
        sys.stdout.flush()
        bndbox = obj.getElementsByTagName("bndbox")[0]
        xMin = int(bndbox.getElementsByTagName("xmin")[0].childNodes[0].data)
        yMin = int(bndbox.getElementsByTagName("ymin")[0].childNodes[0].data)
        xMax = int(bndbox.getElementsByTagName("xmax")[0].childNodes[0].data)
        yMax = int(bndbox.getElementsByTagName("ymax")[0].childNodes[0].data)
        rect = Rectangle((xMin, yMin), xMax - xMin, yMax - yMin)
        rect.set_edgecolor('yellow')
        rect.set_facecolor('none')
        ax.add_patch(rect)
        plt.show(block=False)
        input("")
        rect.remove()
