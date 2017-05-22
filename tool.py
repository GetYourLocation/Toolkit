#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import urllib.request

URL_KCF = 'https://github.com/GetYourLocation/KCFcpp/raw/master/bin/KCF'


def loadKCF():
    kcf_path = os.path.join('bin', 'KCF')
    if os.path.exists(kcf_path):
        print("KCF executable exists at '%s'." % kcf_path)
    else:
        print("Downloading KCF executable...")
        filename, headers = urllib.request.urlretrieve(URL_KCF, kcf_path)
        print("KCF executable loaded to '%s'." % filename)
