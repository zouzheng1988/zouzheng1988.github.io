'''
# debug.py
# using to login to the web
# function :
    login to the web
# version : 0.0.1
# author : wei.meng @ 20180409
'''

import os, sys, requests, traceback

sys.path.append('../System')

from LogShow import LogShow


class LogIn(object):

    def __init__(self, ipadd):
        self.class_name = 'LogIn'
        if isinstance(ipadd, str):
            self.ip = ipadd
        else:
            self.ip = str(ipadd)
        self.url_pre = 'http://' + self.ip
        self.url_login = self.url_pre + '/service/system/login'
        self.data_login = {'name':'admin', 'pw':'admin111'}

        self.ls = LogShow(self.class_name)
    
    def __str__(self):
        return self.class_name

    def login(self):
        try:
            self.ls.log_print('system', 'login to ' + self.ip + ' now', self.login.__name__)
            self.session = requests.Session()
            login = self.session.post(url = self.url_login, data = self.data_login)
            login.raise_for_status()
            self.ls.log_print('system', 'login successful', self.login.__name__)
            self.login_flag = True
            return self.session
        except Exception,e:
            self.ls.log_print('error', str(traceback.print_exc()), self.login.__name__)
            if "('Connection aborted.', BadStatusLine("''",)"  in str(e):
                self.login_flag = True
                return self.session
            else:
                self.login_flag = False
                self.login()

if __name__ == '__main__':
    lg = LogIn('10.16.130.129')
    lg.login()