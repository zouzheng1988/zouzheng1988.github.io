'''
# UnlockSN.py
# date 20171229
# version 0.0.4
# 20180102 : modify - bug fix of readlines
# using windows openssh to get the sn unlock always failed reason : echo command and | command in linux and windows is different
# if the pem file changed, should using new. and the testtool also using this module.
'''


import time, sys, os, json, traceback
import base64
sys.path.append('../System')
from LogShow import LogShow

class UnlockSN(object):
    def __init__(self, sn):
        self.class_name = "UnlockSN"
        self.sn = sn.replace("\n","") + "\n"
        self.localpath = os.path.split(os.path.realpath(__file__))[0]
        self.exepath = os.path.abspath(os.path.join(self.localpath,"..\\..\\win32tools\\openssl_102n\\openssl.exe"))
        self.pempath = os.path.abspath(os.path.join(self.localpath,"..\\pem\\challenge_private.pem"))
        self.sourcepath = ".\\sn.txt"
        self.resultpath = ".\\sign_result.txt"
        self.ls = LogShow(self.class_name)

    def __str__(self):
        return self.class_name

    def sign(self):
        try:
            w = open(self.sourcepath, 'wb')
            w.write(self.sn)
            w.close()
            os.system(self.exepath + " rsautl -sign -inkey " + self.pempath + " -in " + self.sourcepath + " -out " + self.resultpath)
            f = open(self.resultpath, 'rb')
            unlockstrs = ""
            for line in f.readlines():
                unlockstrs = unlockstrs + line
            f.close()
            result = base64.b64encode(unlockstrs)
            return result
        except Exception, e:
            self.ls.log_print('error', str(traceback.print_exc()), self.sign.__name__)