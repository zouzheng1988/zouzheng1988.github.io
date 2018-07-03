'''
# GetDiagnosis.py
# using to get web diagnosis information
# author : wei.meng
# date : 20171023
# version : 0.1.1
'''
import requests
import json
import sys,os
import time
import subprocess,traceback,platform
from LogShow import LogShow
from datetime import datetime

class GetDiagnosis(object):

    def __init__(self,ipadd):
        self.ip = ipadd
        self.url_login = 'http://' + self.ip + '/service/system/login'
        self.url_open = 'http://' + self.ip + '/service/system/diagnosis'
        self.url_status = 'http://' + self.ip + '/service/system/diagnosis/status'
        self.url_msg = 'http://' + self.ip + '/service/system/diagnosis/msg'
        self.data_login = {'name':'admin', 'pw':'admin111'}
        self.ls = LogShow("GetDiagnosis")
        self.msg = ""
        self.found_para = False

    # Login the slamware web Administrator with 'admin' and 'admin111'
    def Login(self):
        try:
            self.session = requests.Session()
            self.ls.log_print("system", '[login] session init, ready to login' )
            login = self.session.post(url=self.url_login,data=self.data_login)
            self.ls.log_print("system",  '[login] ok')
            return True
        except Exception, e:
            self.ls.log_print("system", '[login] failed with ' + str(e))
            return False

    # enable the diagnosis
    def OpenDiagnosis(self):
        try:
            self.ls.log_print("system", '[open] try to open diagnosis')
            data = {"diagnosis":"enable"}
            self.session.post(url=self.url_open, data=data)
            self.ls.log_print("system", '[open] ok')
            return True
        except Exception,e:
            self.ls.log_print("system", '[open] failed with ' + str(e))
            return False

    def getStatusofOpen(self):
        try:
            self.ls.log_print("system", "[status] try to get status of diagnosis")
            status = json.loads(self.session.get(self.url_status).text)
            self.ls.log_print("system", "[status]" + str(status))
            if status["result"] == "success":
                if status["message"] == "ON":
                    self.ls.log_print("system", "[status] ok")
                    return True
                else:
                    self.ls.log_print("system", "[status] open failed")
                    return False
            else:
                self.ls.log_print("system", "[status] open failed")
                return False
        except Exception, e:
            self.ls.log_print("error", "[status] failed with " +str(e))
            return False

    def getMsg(self):
        try:
            self.ls.log_print("system", "[getmsg] try to get diagnosis msg ")
            self.msg = json.loads(self.session.get(self.url_msg).text)
            self.ls.log_print("system", "[getmsg] get diagnosis msg ok")
            time.sleep(10)
            return True
        except Exception, e:
            self.ls.log_print("error", "[getmsg] failed with " +str(e))
            return False

    def WriteToFile(self,filename,content,writetofile):
        try:
            self.ls.log_print("system", "[WriteToFile] write to file " + filename)
            self.found_para = True
            if not writetofile :
                return content
            File = open(filename, 'w')
            File.write(json.dumps(content))
            File.close()
            self.ls.log_print("system", "[WriteToFile] write to file success")
        except Exception, e:
            self.ls.log_print("error", "[WriteToFile] " + str(e))


    def RunGetAll(self,para="all",writetofile=False,filename="./diagnosis.txt"):
        try:
            while True:
                if self.Login():
                    if self.getStatusofOpen():
                        if self.getMsg():
                            if para in "all" and (not writetofile):
                                self.WriteToFile(filename, self.msg, writetofile)
                                break
                            else:
                                for m in self.msg :
                                    self.ls.log_print("debug", m)
                                    if para in m["diagnosis_info_type"]:
                                        self.WriteToFile(filename, m, writetofile)
                                        break
                                    if para in m["diagnosis_info_type"]:
                                        self.WriteToFile(filename, m, writetofile)
                                        break
                                    if para in m["diagnosis_info_type"]:
                                        self.WriteToFile(filename, m, writetofile)
                                        break
                            if self.found_para :
                                break 
                            else :
                                continue
                        else:
                            time.sleep(5)
                            continue
                    else :
                        if self.OpenDiagnosis():
                            time.sleep(5)
                        else:
                            time.sleep(5)
                            continue
                        continue
                else :
                    time.sleep(5)
                    continue
        except Exception, e:
            self.ls.log_print("error", "[rungetmsg] failed with " +str(e))

if __name__ == "__main__":
    gd = GetDiagnosis("10.16.130.41")
    try:
        gd.RunGetAll(para="DiagnosInfoLidarScan",writetofile=True, filename="./diagnosis.txt")
    except Exception, e:
        print e
