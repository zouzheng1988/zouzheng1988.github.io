'''
# getSN.py
# using to get sn with web service url
# function :
    1, get sn json files
    2, get Device SN
    3, get Zeus Base SN
    4, get IP MODE
    5, get Version
    6, get FWversion
# author : wei.meng @ 20180409
# version : 0.0.2
# modify : wei.meng @ 20180604 using functools.wraps(func) , delete __name__

'''

import os, json ,sys, time, requests, traceback

sys.path.append('../System')

from LogShow import LogShow
from login import LogIn
import functools


### this checkSN function is for checking the session is ok or None
def checkSN(func):
    @functools.wraps(func)
    def wapper(self):
        if self.session is None:
            self.session = self.reLogin()
        #wapper.__name__ = func.__name__
        return func(self)
    return wapper

class GetSN(object):

    def __init__(self, ipadd, session):
        self.class_name = 'GetSN'
        

        if isinstance(ipadd, str):
            self.ip = ipadd
        else:
            self.ip = str(ipadd)
        
        self.login = LogIn(self.ip)

        if session is not None:
            self.session = session
        else:
            self.session = self.reLogin()

        url_pre = 'http://' + self.ip
        self.url_sn = url_pre + '/service/system/admin/sn'
        self.url_version = url_pre + '/service/system/firmware_upgrade/version'
        
        self.ls = LogShow(self.class_name)
        self.getContent()


    def __str__(self):
        return self.class_name


    def reLogin(self):
        return  self.login.login()

    @checkSN
    def getContent(self):
        try:
            self.SNcontent = self.session.get(self.url_sn).text
            self.snJson = json.loads(self.SNcontent)
            time.sleep(5)
            self.VEcontent = self.session.get(self.url_version).text
            self.veJson = json.loads(self.VEcontent)
        except Exception,e:
            self.ls.log_print('error', str(traceback.print_exc()), self.getContent.__name__)
            time.sleep(5)
            self.getContent()
            
    # getDeviceSN
    @checkSN
    def getDeviceSN(self):
        try:
            if self.snJson.has_key('DeviceSN'):
                self.sn = self.snJson['DeviceSN']
            else:
                self.sn = None
            self.ls.log_print('system', 'Device sn is ' + self.sn, self.getDeviceSN.__name__)            
            return self.sn
        except Exception,e:
            self.ls.log_print('error', str(traceback.print_exc()), self.getDeviceSN.__name__)
    
    # getzeusBaseSN
    @checkSN
    def getBaseSN(self):
        try:
            if self.snJson.has_key('Base(zeus base) SN'):
                self.basesn = self.snJson['Base(zeus base) SN']
            if self.snJson.has_key('Base(ref base) SN'):
                self.basesn = self.snJson['Base(ref base) SN']
            
            self.ls.log_print('system', 'Base sn is ' + self.basesn, self.getBaseSN.__name__)
            return self.basesn
        except Exception,e:
            self.ls.log_print('error', str(traceback.print_exc()), self.getBaseSN.__name__)
    
    # getIpMode
    @checkSN
    def getIPMode(self):
        try:
            if self.snJson.has_key('MODE : SSID : IP'):
                self.ipmode = self.snJson['MODE : SSID : IP']
            else:
                self.ipmode = None
            self.ls.log_print('system', 'ipmode is ' + self.ipmode, self.getIPMode.__name__)
            return self.ipmode
        except Exception,e:
            self.ls.log_print('error', str(traceback.print_exc()), self.getIPMode.__name__)

    # getVersion
    @checkSN
    def getVersion(self):
        try:
            if self.veJson.has_key('FWVERSION'):
                self.version = self.veJson['FWVERSION']
            else:
                self.version = None
            self.ls.log_print('system', 'version is ' + self.version, self.getVersion.__name__)
            return self.version
        except Exception,e:
            self.ls.log_print('error', str(traceback.print_exc()), self.getVersion.__name__)

    # getFWVersions
    @checkSN
    def getFWVersion(self):
            return self.veJson

    # get ALL
    def run(self, command):
        try:
            if command is not None and command != '':
                if command == 'getDeviceSN':
                    return self.getDeviceSN()
                if command == 'getBaseSN':
                    return self.getBaseSN()
                if command == 'getIPMode':
                    return self.getIPMode()
                if command == 'getVersion':
                    return self.getVersion()
                if command == 'getFWVersion':
                    return self.getFWVersion()

        except Exception,e:
            self.ls.log_print('error', str(traceback.print_exc()), self.run.__name__)
        