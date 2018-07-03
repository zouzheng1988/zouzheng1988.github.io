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
#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import urllib2
import json
import sys
import time
import os
from LogShow import LogShow

class GetVersion(object):

    def __init__(self,ipadd):
        self.name = "GetVersion"
        self.ip = ipadd
        self.content = str()
        self.url_login = 'http://' + self.ip + '/service/system/login'
        self.url_version = "http://" + self.ip + "/service/system/firmware_upgrade/version"
        self.data_login = {'name':'admin', 'pw':'admin111'}
        self.ls = LogShow(self.name)

    def save_content(self):
        func_name = "save_content"
        self.session = requests.Session()
        while True:
            try:
                self.session.post(url=self.url_login,data=self.data_login) 
            except:
                self.ls.log_print("system", "[" + func_name + "] waitting for login successfully")
                time.sleep(10)
                continue
            break
        while True:
            try:
                self.content = self.session.get(self.url_version).text
            except:
                self.ls.log_print("system", "[" + func_name + "] waitting for login successfully")
                time.sleep(10)
                continue
            break

    def getversion(self):
        func_name = "getversion"
        while True:
            try:
                self.version = json.loads(self.content)["FWVERSION"]
                return self.version
            except:
                self.ls.log_print("system", "[" + func_name + "] wrong")
                time.sleep(10)
                continue
            break

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
            

    def  RunCheck(self,version_name):
        func_name = "RunCheck"
        try:
            self.save_content()
            self.getversion()
            self.splitversion()
            self.compare(version_name)
        except Exception,e:
            self.ls.log_print("system", "[" + func_name + "]< error > wrong with error : " + str(e))
            sys.exit(1)
    
    def RunCheck_1(self,version_name):
        func_name = "RunCheck_1"
        try :
            self.save_content()
            self.getversion()
            self.splitversion()
            self.compare_cannotdown(version_name)
        except Exception,e:
            self.ls.log_print("system", "[" + func_name + "-1]< error > wrong with error : " + str(e))
            sys.exit(1)
# sdp_edison.2.2.1_rtm.20170301.bin
# 2.2.1_rtm-sdp-20170301
