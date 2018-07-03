'''
# WebController.py
# using to control the web with service url
# functions :
    1, web page login
    2, open debug
    3, close debug
    4, get sn json
    5, get version
    6, get diagnosis
    7, open diagnosis
# author : wei.meng
# version : 0.0.1
# date : 20180409
'''

import os, sys, time, json, requests, traceback, platform

sys.path.append('../System')
from login import LogIn
from LogShow import LogShow
from Debug import Debug
from getSN import GetSN
from getDiagnosis import GetDiagnosis
from Update import Update

class WebController(object):

    def __init__(self, ipadd, session=None):
        self.ip = ipadd
        self.class_name = "WebController"
        self.ls = LogShow(self.class_name)
        if not hasattr(self, "session"):
            if session is None:
                self.login()
            else:
                self.session = session

    def __str__(self):
        return self.class_name

    def login(self):
        self.login = LogIn(self.ip)
        self.session = self.login.login()
        return self.session
    
    def Debug(self):
        if not hasattr(self, "debug"):
            self.debug = Debug(self.ip, self.session)
        return self.debug

    def openDebug(self):
        self.Debug()
        return self.debug.openDebug()
            
    def closeDebug(self):
        self.Debug()
        return self.debug.closeDebug()
    
    def getSN(self):
        if not hasattr(self, "getsn"):
            self.getsn = GetSN(self.ip, self.session)
        return self.getsn

    def getDeviceSN(self):
        self.getSN()
        return self.getsn.getDeviceSN()

    def getBaseSN(self):
        self.getSN()
        return self.getsn.getBaseSN()
    
    def getIPMode(self):
        self.getSN()
        return self.getsn.getIPMode()
    
    def getVersion(self):
        self.getSN()
        return self.getsn.getVersion()

    def getFWVersion(self):
        self.getSN()
        return self.getsn.getFWVersion()

    def GetDiagnosis(self):
        if not hasattr(self, "getdiagnosis"):
            self.getdiagnosis = GetDiagnosis(self.ip, self.session)
        return self.getdiagnosis

    def OpenDiagnosis(self):
        self.GetDiagnosis()
        self.getdiagnosis.OpenDiagnosis()
    
    def getMsg(self):
        self.GetDiagnosis()
        self.getdiagnosis.getMsg()
    
    def RunGetAll(self):    
        self.GetDiagnosis()
        self.getdiagnosis.RunGetAll()

    def CloseDiagnosis(self):
        self.GetDiagnosis()
        self.getdiagnosis.CloseDiagnosis()
    
    def Update(self, fmpath):
        if not hasattr(self, "update"):
            self.update = Update(self.ip, fmpath, self.session)
        return self.update
    
    def runUpdate(self):
        self.Update()
        self.update.runUpdate()
    
    def runUpdate_new(self):
        self.Update()
        self.update.runUpdate_new()

    def run(self, command, args=[]):
        if command is not None and command != '':
            if command == 'openDebug':
                self.openDebug()
            if command == 'closeDebug':
                self.closeDebug()
            if command == 'getDeviceSN':
                self.getDeviceSN()
            if command == 'getBaseSN':
                self.getBaseSN()
            if command == 'getVersion':
                self.getVersion()
            if command == 'getFWVersion':
                self.getFWVersion()
            if command == 'openDiagnosis':
                self.openDiagnosis()
            if command == 'getMsg':
                self.getMsg()
            if command == 'RunGetALL':
                self.RunGetAll()
            if command == 'CloseDiagnosis':
                self.CloseDiagnosis()
            if command == 'Update':
                self.Update(args)
            if command == 'runUpdate':
                self.runUpdate()

if __name__ == '__main__':
    wc = WebController('10.16.130.129')
    wc.run('openDebug')
    time.sleep(2)
    wc.run('closeDebug')
    time.sleep(1)
    wc.getDeviceSN()
    wc.getBaseSN()
    wc.getVersion()
    wc.getFWVersion()
    
    wc.RunGetAll()
    wc.CloseDiagnosis()