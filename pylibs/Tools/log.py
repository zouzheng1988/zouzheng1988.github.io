# encoding='utf-8'

'''
# log.py - AutoTestLog()
# date : 20170811
# version : 0.1
# author : wei.meng
# 20170811 - need add movie camera (ipc)
'''

import time
import os,sys
sys.path.append('../Onlineslam')
sys.path.append('../System')

from SSH import Ssh
from Sftp import Sftp
from LogShow import LogShow
from IpcControl import getVideoLog
#from slamwaredControl import SlamwaredControl

class AutoTestLog(object):

    def __init__ (self, logflag):
        self.logflag = logflag
        self.log_setup()
        self.user = "root"
        self.password = "slamware123"

    def log_setup(self):    
        self.ls = LogShow(self.logflag)

    def log_print(self, rank, log_str):
        self.ls.log_print(rank, log_str)

    def log_getpypath(self):
        self.log_pypath = sys.path[0]
        print self.log_pypath

    def log_change_service(self, ip, user, password):
        self.sc  = SlamwaredControl( ip, user, password)
        self.ls.log_print("debug", "open zeus stms log (replace the service file)")
        self.sc.stopslamwared()
        time.sleep(5)
        sftp = Sftp(ip)
        sftp.Connect()
        sftp.PutFile("../../../base/tools/config/slamwared.service" , "/lib/systemd/system/slamwared.service")
        sftp.Close()
        time.sleep(3)
        self.sc.rmstmslog()
        time.sleep(3)
        self.sc.reloadslamwared()
        time.sleep(3)
        self.sc.startslamwared()
        time.sleep(30)

    def log_get_stms(self, ip, log_local_name):
        self.log_print("system", "get stms log file")
        self.sc.stopslamwared()
        remote_stms_path = "/home/root/slamware.stms"
        local_stms_path = ".\\log\\" + log_local_name
        sftp = Sftp(ip)
        sftp.Connect()
        sftp.GetFile(remote_stms_path,local_stms_path)
        self.log_print("system", "get stms log file OK")
        self.sc.startslamwared()

    def log_get_systemlog(self, ip, logname):
        ssh = Ssh(ip, self.user, self.password)
        ssh.Exec("journalctl > /home/root/system.log")          
        ssh.Close()
        self.ls.log_print("system", "[getlog] start get log")
        sf = Sftp(ip)
        sf.GetFile("/home/root/system.log","log\\"+logname)            
        # sf.GetFile("/home/root/slamware.stms","log\\slamawre.stms")
        sf.Close()


    def log_start_video_record(self, logpath):
        #url="rtsp://admin:Admin123@10.16.129.14/h264/Channel/1"
        url = "10.16.129.121"
        user = "admin"
        password = "Admin123"
        self.ipclog = getVideoLog(url, user, password, logpath)
        self.ipclog.startlog()


    def log_stop_video_record(self):
        self.ipclog.stoplog()


    def log_get_video(self, camera_ip, moive_path):
        self.log_print("system", "get movie log now ")

    def log_get_systemlog(self, ip, log_local_name):
        self.log_print("system", "get system log")
        
    

if __name__ == "__main__" :
    atl = AutoTestLog("Test")
    atl.log_print("error","wrong with Test") 
    #atl.log_change_service("192.168.11.1", "root", "slamware123")
    #atl.log_get_stms("192.168.11.1","test.stms")
    atl.log_getpypath()