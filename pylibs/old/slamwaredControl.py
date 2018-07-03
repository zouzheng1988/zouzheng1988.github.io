# encoding='utf-8'

'''
# log.py - SlamWaredControl()
# date : 20170811
# version : 0.1
# author : wei.meng
# 20170823 - the slamwared control libs (ipc) , must have the ssh connect 
'''
import os,time,sys

from datetime import datetime
from LogShow import LogShow
from SSH import Ssh,Sftp

class SlamwaredControl(object):
    def __init__(self,ip,user,password):
        self.logflag = "Slamwared Control"
        self.ls = LogShow(self.logflag)
        self.ip = ip
        self.ssh = Ssh(ip,user,password)
        self.ssh.Connect()

    def startslamwared(self):
        self.ls.log_print("system", "start the slamwared on " + str(self.ip))
        self.ssh.Exec("systemctl start slamwared")
        self.ls.log_print("system", "start the slamwared success")


    def stopslamwared(self):
        self.ls.log_print("system", "stop the slamwared on " + str(self.ip))
        self.ssh.Exec("systemctl stop slamwared")
        self.ls.log_print("system", "stop the slamwared success")
    
    def reloadslamwared(self):
        self.ls.log_print("system", "reload the slamwared on " + str(self.ip))
        self.ssh.Exec("systemctl daemon-reload")
        self.ls.log_print("system", "reload the slamwared success")

    def rmstmslog(self):
        self.ls.log_print("system", "remove the log of stms on " + str(self.ip))
        self.ssh.Exec("if [ -f /home/root/slamware.stms ]; then rm /home/root/slamware.stms fi")
        self.ls.log_print("system", "remove the log of stms success")