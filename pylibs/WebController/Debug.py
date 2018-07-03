'''
# debug.py
# using to open/close debug mode with web service url
# function :
    1, open debug mode
    2, close debug mode
# version : 0.0.1
# author : wei.meng @ 20180409
'''

import requests
import json
import sys, os, time, traceback, platform

sys.path.append("../System")

from LogShow import LogShow
from UnlockSN import UnlockSN
from login import LogIn
from getSN import GetSN


def checkSN(func):
    def wapper(self):
        if self.session is None:
            self.session = self.reLogin()
        wapper.__name__ = func.__name__
        return func(self)
    return wapper

class Debug(object):
    
    def __init__(self, ipadd, session):
        if isinstance(ipadd, str):
            self.ip = ipadd
        else:
            self.ip = str(ipadd)

        if session is not None:
            self.session = session
        else:
            self.session = self.reLogin()
        self.class_name = "Debug"
        self.url_pre = 'http://' + self.ip
        self.url_open_debug = self.url_pre + '/service/system/admin/challenge'
        self.url_close_debug = self.url_pre + '/service/system/admin/unroot'

        self.ls = LogShow(self.class_name)
    
    def __str__(self):
        return self.class_name

    def reLogin(self):
        login = LogIn(self.ip)
        return login.login()
    
    @checkSN
    def openDebug(self):
        try:
            getsn = GetSN(self.ip, self.session)
            sn = getsn.getDeviceSN()
            unlock = UnlockSN(sn)
            snunlock = unlock.sign()
            self.ls.log_print('system', 'unlock sn is ' + str(snunlock), self.openDebug.__name__)
            data_unlock = {'cha-token':snunlock}
            self.session.post(url = self.url_open_debug, data = data_unlock)
            self.ls.log_print('system', 'open debug ok', self.openDebug.__name__)
            return True
        except Exception,e:
            self.ls.log_print('error', str(traceback.print_exc()), self.openDebug.__name__)
            if "BadStatusLine" in str(e):
                return True
            else:
                time.sleep(5)
                self.openDebug()
            
    @checkSN
    def closeDebug(self):
        try:
            self.session.post(url = self.url_close_debug)
            self.ls.log_print('system', ' close debug ok', self.closeDebug.__name__)
            return True
        except Exception,e:
            self.ls.log_print('error', str(traceback.print_exc()), self.closeDebug.__name__)
            if "BadStatusLine" in str(e):
                return True
            else:
                time.sleep(5)
                self.openDebug()
            