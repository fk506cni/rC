#!/usr/bin/env python3
# coding: utf-8

from time import sleep
import sys
import os
import pandas as pd

argvs = sys.argv
from rc1.file1 import Fl
from rc1.file1 import Fs

#check dir or file


if os.path.isdir(argvs[1]):
    print("this is directory")
    # fs = os.listdir(argvs[1])
    # for f in fs:
    #     print(f)

    fs = Fs(argvs[1])
    fs.getFileInfoS()
    fs.zipDir()

elif os.path.isfile(argvs[1]):
    print("this is file")
    print(argvs[1])

    fl = Fl(argvs[1])
    fl.getFileInfo()
    fl.makeDir4Zip()
    fl.saveDF()
    fl.cpFile()
    #fl.zipDir()
    fl.zipDir(andrm=True)


for i in range(10):
    print("waiting...")
    for arg in argvs:
        print(arg)

    sleep(1)
