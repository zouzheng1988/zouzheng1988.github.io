'''
# use urllib2 to get the content of web ; 
# get the version from json data ;
# version : 1.5
# author : mengwei 
# modify : 2017.3.1 - add new function
# modify : 2017.3.2 - add output to file (succesful and fail)
# modify : 2017.3.6 - maybe change the names to one name
# modify : 2017.3.27 - add check the flash wrong build 
# modify : 2017.5.23 - add new check function : when this version can not be downgrade , use this check .
# modify : 2017.8.14 - use LogShow lib
# modify : rewrite at 20180320
'''

'''
# Checkversion.py
# using to check the web version and  bin version
# function:
    1, compare versions
    2, run check
# author : wei.meng @ 20180412
'''
#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import urllib2
import json
import sys
import time
import os

sys.path.append('../System')

from LogShow import LogShow
from Check import Check

sys.path.append('../WebController')

from WebController import WebController

class Checkversion(object):

    def __init__(self,ipadd, session=None):
        self.class_name = 'GetVersion'
        self.ls = LogShow(self.class_name)

        if isinstance(ipadd, str):
            self.ip = ipadd
        else:
            self.ip = str(ipadd)
        if not Check.checkIP(self.ip):
            self.ls.log_print('warn', self.ip + ' is not valuable', '__init__')
        self.webcontroller = WebController(self.ip, session)
        
    def getversion(self):
       self.version = self.webcontroller.getVersion()
       return self.version

    def splitversion(self):
        if self.version is not None:
            self.version_num,self.v_sdp,self.version_date = self.version.split('-')

    def compare(self, version_name):
        func_name = "compare"
        self.ls.log_print("system", "[" + func_name + "] firmware version is : " + version_name)
        self.ls.log_print("system", "[" + func_name + "] current  version is : " + self.version_num  + " " + self.version_date)
        
        if self.version_date in version_name :
            if self.version_num in version_name:
                self.ls.log_print("system", "[" + func_name + "][--- update successful (version number and date is right !)--- ]")
                os.system("echo successful > compare")
            else :
                self.ls.log_print("system", "[" + func_name + "]< error > version number check fail")
                os.system("echo fail > compare")
                sys.exit(1)
                
        else :
            self.ls.log_print("system", "[" + func_name + "]< error > verison date check fail")
            os.system("echo fail > compare")
            sys.exit(1)
            
        
    def compare_cannotdown(self,version_name):
        func_name = "compare-cannotdown"
        self.ls.log_print("system", "[" + func_name + "] not-downgrade version check running")
        self.ls.log_print("system", "[" + func_name + "] before   version is : " + version_name)
        self.ls.log_print("system", "[" + func_name + "] current  version is : " + self.version_num + " " + self.version_date)
        if self.version_date in version_name :
            if self.version_num in version_name:
                self.ls.log_print("system", "[" + func_name + "][--- update failed (version name and num is right , should not be downgrade !)  ---] ")
                os.system("echo fail > compare1")
                sys.exit(1)
            else:
                self.ls.log_print("system", "[" + func_name + "]< successful > version check OK")
                os.system("echo successful > compare1")                
        else :
            self.ls.log_print("system", "[" + func_name + "]< successful > version check OK")
            os.system("echo successful > compare1")
            

    def RunCheck(self,version_name):
        func_name = "RunCheck"
        try:
            self.getversion()
            self.splitversion()
            self.compare(version_name)
        except Exception,e:
            self.ls.log_print("system", "[" + func_name + "]< error > wrong with error : " + str(e))
            sys.exit(1)
    
    def RunCheck_1(self,version_name):
        func_name = "RunCheck_1"
        try :
            self.getversion()
            self.splitversion()
            self.compare_cannotdown(version_name)
        except Exception,e:
            self.ls.log_print("system", "[" + func_name + "-1]< error > wrong with error : " + str(e))
            sys.exit(1)
# sdp_edison.2.2.1_rtm.20170301.bin
# 2.2.1_rtm-sdp-20170301
