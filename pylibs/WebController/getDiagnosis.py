'''
# getDiagnosis.py
# using to get Diagnosis informations
# function :
    1, get diagnosis 
# version : 0.0.2
# author : wei.meng @ 20180409
# modify : wei.meng @ 20180604 using th functools.wraps(func) , delete __name__
'''
import requests
import json
import sys,os
import time
import subprocess,traceback,platform
sys.path.append('../System')

from LogShow import LogShow
from datetime import datetime
from login import LogIn
import functools


def checkSN(func):
    @functools.wraps(func)
    def wapper(self):
        if self.session is None:
            self.session = self.reLogin()
        #wapper.__name__ = func.__name__
        return func(self)
    return wapper

class GetDiagnosis(object):

    def __init__(self, ipadd, session):
        if isinstance(ipadd, str):
            self.ip = ipadd
        else:
            self.ip = str(ipadd)
        if isinstance(session, requests.Session):
            self.session = session
        else:
            self.session = self.reLogin()
        self.class_name = 'GetDiagnosis'
        url_pre = 'http://' + self.ip
        self.url_open = url_pre + '/service/system/diagnosis'
        self.url_status = url_pre + '/service/system/diagnosis/status'
        self.url_msg = url_pre + '/service/system/diagnosis/msg'
        self.url_close = self.url_open

        self.ls = LogShow(self.class_name)
        self.msg = ""
        self.found_para = False

        self.open_data = {'diagnosis':'enable'}
        self.close_data = {'diagnosis':'disable'}

    def __str__(self):
        return self.class_name

    def reLogin(self):
        login = LogIn(self.ip)
        return login.login()

    @checkSN
    def OpenDiagnosis(self):
        try:
            self.ls.log_print("system", 'try to open diagnosis', self.OpenDiagnosis.__name__)
            self.session.post(url=self.url_open, data=self.open_data)
            self.ls.log_print("system", 'ok', self.OpenDiagnosis.__name__)
            return self.getStatusofOpen()
        except Exception,e:
            self.ls.log_print("system", str(traceback.print_exc()), self.OpenDiagnosis.__name__)
            return False

    @checkSN
    def getStatusofOpen(self):
        try:
            self.ls.log_print("system", "try to get status of diagnosis", self.getStatusofOpen.__name__)
            jsonbefore = self.session.get(self.url_status).text
            if jsonbefore is not None and jsonbefore != "":
                status = json.loads(jsonbefore)
            else:
                status = None
                return False
            self.ls.log_print("system", "status:" + str(status), self.getStatusofOpen.__name__)
            if status["result"] == "success":
                if status["message"] == "ON":
                    self.ls.log_print("system", "[status] ok", self.getStatusofOpen.__name__)
                    return True
                else:
                    self.ls.log_print("system", "[status] open failed", self.getStatusofOpen.__name__)
                    return False
            else:
                self.ls.log_print("system", "[status] open failed", self.getStatusofOpen.__name__)
                return False
        except Exception, e:
            self.ls.log_print("error", str(traceback.print_exc()), self.getStatusofOpen.__name__)
            return False 

    @checkSN       
    def getStatusofClose(self):
        try:
            self.ls.log_print("system", "try to get status of diagnosis", self.getStatusofClose.__name__)
            jsonbefore = str(self.session.get(self.url_status).text)
            self.ls.log_print('debug', jsonbefore)
            if jsonbefore is not None and jsonbefore != "":
                status = json.loads(jsonbefore)
            else:
                status = None
            self.ls.log_print("system", "status:" + str(status), self.getStatusofClose.__name__)
            if status["result"] == "success":
                if status["message"] == "OFF":
                    self.ls.log_print("system", "[status] ok", self.getStatusofClose.__name__)
                    return True
                else:
                    self.ls.log_print("system", "[status] close failed", self.getStatusofClose.__name__)
                    return False
            else:
                self.ls.log_print("system", "[status] close failed", self.getStatusofClose.__name__)
                return False
        except Exception, e:
            self.ls.log_print("error", str(traceback.print_exc()), self.getStatusofClose.__name__)
            return False

    @checkSN
    def getMsg(self):
        try:
            self.ls.log_print("system", "try to get diagnosis msg ", self.getMsg.__name__)
            jsonbefore = self.session.get(self.url_msg).text
            print jsonbefore
            if jsonbefore is not None and jsonbefore != "":
                self.msg = json.loads(jsonbefore)
            else:
                self.msg = None
                return False
            self.ls.log_print("system", "get diagnosis msg ok", self.getMsg.__name__)
            time.sleep(10)
            return True
        except Exception, e:
            self.ls.log_print("error", str(traceback.print_exc()), self.getMsg.__name__)
            return False

    def WriteToFile(self, filename, content, writetofile):
        try:
            self.ls.log_print("system", "write to file " + filename, self.WriteToFile.__name__)
            self.found_para = True
            if not writetofile :
                return content
            File = open(filename, 'a')
            File.write(json.dumps(content))
            File.close()
            self.ls.log_print("system", "write to file success", self.WriteToFile.__name__)
        except Exception, e:
            self.ls.log_print("error", str(traceback.print_exc()), self.WriteToFile.__name__)

    def RunGetAll(self,para="all",writetofile=True,filename="./diagnosis.txt"):
        try:
            self.CloseDiagnosis()
            self.OpenDiagnosis()
            self.ls.log_print('debug', self.getStatusofOpen(), self.RunGetAll.__name__)
            if self.getStatusofOpen() is True:
                time.sleep(5)
                self.ls.log_print('debug', 'here is get msg before', self.RunGetAll.__name__)
                if self.getMsg():
                    self.WriteToFile(filename, self.msg, writetofile)                    
                else:
                    time.sleep(5)
            else:
                self.OpenDiagnosis()
        except Exception, e:
            self.ls.log_print("error", str(traceback.print_exc()), self.RunGetAll.__name__)

    @checkSN
    def CloseDiagnosis(self):
        try:
            self.ls.log_print("system", 'try to close diagnosis', self.CloseDiagnosis.__name__)
            self.session.post(url=self.url_close, data=self.close_data)
            self.ls.log_print("system", 'ok', self.CloseDiagnosis.__name__)
            return self.getStatusofClose()
        except Exception,e:
            self.ls.log_print("system", str(traceback.print_exc()), self.CloseDiagnosis.__name__)
            return False