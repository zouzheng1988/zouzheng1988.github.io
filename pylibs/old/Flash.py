#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
author : wei.meng
date : 2017.03.09
version : 1.0
'''
import sys
import os
import time
from LogShow import LogShow

class Flash(object):
    def __init__(self):
        self.ls = LogShow("Root")
        self.ls.log_print("system", "[Flash]")

    def fileExist(self,filepath):
        return os.path.exists(filepath)

    def getEnv(self,envname):
        try:
            if envname != None and envname != "":
                return os.getenv(envname)
            else:
                return ""
        except Exception,e:
            self.ls.log_print("error", "[getenvv] failed with " + envname)
            return ""

    def getFileName(self,filepath):
        filename=None
        for x in filepath.split("\\"):
            filename = x
        return filename


if __name__ == "__main__":

    try:

        envname = "NAME_OF_ONEBUILD"
        flash = Flash()
        filepath = flash.getEnv(envname)
        filename = flash.getFileName(filepath)
        print filename
    except:
        print ("wrong with ??")
