#!/usr/bin/env python3
# coding: utf-8

import os
import pandas as pd
import hashlib
import datetime
import re
import shutil

class Fl:
    f_str = ""
    df = pd.DataFrame()

    dir_name = ""
    anot_path = ""

    def __init__(self, filepath):
        self.f_str = filepath
        print("processing files is...")
        print(self.f_str)

    def getFileInfo(self):
        fi = os.stat(self.f_str)
        #shs_md5 = hs.md5(self.f_str).hexdigest()
        #fn = os.path(self.f_str)
        print(fi)
        print(fi.st_size)
        hs = self.getHashAsInt()
        fi_dict = {"st_mode":fi.st_mode, "st_ino":fi.st_ino, "st_dev":fi.st_dev,
                   "md5":hs,
                   "name":os.path.basename(self.f_str),
                   "extension": os.path.splitext(self.f_str)[1]}
        #print(fi_dict)
        ds = pd.Series(fi_dict)
        df = pd.DataFrame([ds], index= [os.path.basename(self.f_str)])
        # df = pd.concat(ds, ds)
        #
        print(ds)
        print(df)
        self.df = self._colsort(df)
        print(self.df)
        # print(df)
        #return fi_dict

    def makeDir4Zip(self):
        dir_name = os.path.basename(self.f_str)
        dir_name = re.sub('.[a-z0-9]*$', "", dir_name)
        print(dir_name)
        dir_name = dir_name + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        print(dir_name)
        dir_name = os.path.dirname(self.f_str)+"\\"+dir_name
        print(dir_name)
        print(os.path.dirname(self.f_str))
        self.dir_name = dir_name
        os.makedirs(dir_name)

    def saveDF(self):
        self.anot_path = self.dir_name+"\\annot.tsv"
        print(self.anot_path)
        df = self.df
        df.to_csv(self.anot_path, sep="\t", encoding="utf-8-sig",index=False)

    def cpFile(self):
        shutil.copy(self.f_str, self.dir_name)
        print("copied!")

    def zipDir(self, andrm = False):
        shutil.make_archive(self.dir_name, "zip", self.dir_name)
        if andrm:
            shutil.rmtree(self.dir_name)

    def getHashAsInt(self):
        md5 = hashlib.md5()
        with open(self.f_str, 'rb') as f:
            for chunk in iter(lambda: f.read(4096 * md5.block_size), b''):
                md5.update(chunk)
        checksum = md5.hexdigest()
        return checksum

        #print(fi.__getattribute__("st_sizes"))
        #print(fi.st_sizes())

    def _colsort(self, df):
        df1 = df.copy()
        cols = list(df.columns.values).copy()
        cols.sort()
        df1 = df1.loc[:, cols]
        return df1

class Fs:
    files = []
    df = pd.DataFrame()
    dir_name = ""
    anot_path = ""

    def __init__(self, dir):
        self.dir_name = dir
        self.files = os.listdir(dir)
        print(self.files)

    def getFileInfoS(self):
        fileInd = []
        ser_ls = []
        for f in self.files:
            f_path = self.dir_name + "\\" + f
            print("path is .")
            print(f_path)
            if os.path.isfile(f_path):
                fi = os.stat(f_path)
                print(fi)
                hs = self.getHashAsInt(f_path)
                print(hs)
                fi_dict = {"st_mode": fi.st_mode, "st_ino": fi.st_ino, "st_dev": fi.st_dev,
                           "md5": hs,
                           "name": os.path.basename(f_path),
                           "extension": os.path.splitext(f_path)[1]}
                ds = pd.Series(fi_dict)
                ser_ls.append(ds)
                fileInd.append(os.path.basename(f_path))
                print(fi_dict)
                print(fi)

        df = pd.DataFrame(ser_ls, index=fileInd)
        print(df)
        self.df = self._colsort(df)
        annot_path = self.dir_name + "\\annot.tsv"
        self.df.to_csv(annot_path, sep="\t", encoding="utf-8-sig",index=False)


    def getHashAsInt(self, f_path):
        md5 = hashlib.md5()
        print(f_path)
        with open(f_path, 'rb') as ff:
            for chunk in iter(lambda: ff.read(4096 * md5.block_size), b''):
                md5.update(chunk)
        checksum = md5.hexdigest()
        return checksum

    def _colsort(self, df):
        df1 = df.copy()
        cols = list(df.columns.values).copy()
        cols.sort()
        df1 = df1.loc[:, cols]
        return df1

    def zipDir(self, andrm = False):
        shutil.make_archive(self.dir_name, "zip", self.dir_name)
        if andrm:
            shutil.rmtree(self.dir_name)