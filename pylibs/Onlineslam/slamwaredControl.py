# encoding='utf-8'

'''
# slamwaredControl.py
# using to control onlineslam with ssh
# function :
    1, start slamwared
    2, stop slamwared
    3, reload service slamwared
    4, remove slamwared stms log file
    5, get motor
# date : 20170811
# version : 0.2
# author : wei.meng
'''
import os,time,sys
from datetime import datetime

sys.path.append('../System')

from LogShow import LogShow
from SSH import Ssh
from Sftp import Sftp

class SlamwaredControl(object):
    def __init__(self):
        self.class_name = "SlamwaredControl"
        self.ls = LogShow(self.class_name)
        self.ssh_flag = False
        self.sftp_flag = False
        

    def __str__(self):
        return self.class_name
    
    def getSSH(self, ipadd, username, password):
        if isinstance(ipadd, str):            
            self.sship = ipadd    
            self.ip = ipadd   
        else:
            self.sship = str(ipadd)
            self.ip = str(ipadd)
        if isinstance(username, str):
            self.sshusername = username
        else:
            self.sshusername = str(username)
        if isinstance(password, str):
            self.sshpassword = password
        else:
            self.sshusername = str(password)

        self.ssh = Ssh(self.sship, self.sshusername, self.sshpassword)
        self.ssh.Connect()
        self.ssh_flag = True

    def getSftp(self, ipadd, username, password):
        if isinstance(ipadd, str):            
            self.sftpip = ipadd       
            self.ip = ipadd
        else:
            self.sftpip = str(ipadd)
            self.ip = str(ipadd)
        if isinstance(username, str):
            self.sftpusername = username
        else:
            self.sftpusername = str(username)
        if isinstance(password, str):
            self.sftppassword = password
        else:
            self.sftppassword = str(password)
        self.sftp = Sftp(self.sftpip, self.sftpusername, self.sftppassword)
        self.sftp.Connect()
        self.sftp_flag = True

    def startslamwared(self):
        self.ls.log_print("system", "start the slamwared on " + str(self.ip), self.startslamwared.__name__)
        self.ssh.Exec("systemctl start slamwared")
        self.ls.log_print("system", "start the slamwared success", self.startslamwared.__name__)

    def getstatusSlamwared(self):
        self.ls.log_print("system", "start get the status", self.getstatusSlamwared.__name__)
        output = str(self.ssh.Exec('systemctl status slamwared'))
        self.ls.log_print('system', output, self.getstatusSlamwared.__name__)

    def stopslamwared(self):
        self.ls.log_print("system", "stop the slamwared on " + str(self.ip), self.stopslamwared.__name__)
        self.ssh.Exec("systemctl stop slamwared")
        self.ls.log_print("system", "stop the slamwared success", self.stopslamwared.__name__)
    
    def reloadslamwared(self):
        self.ls.log_print("system", "reload the slamwared on " + str(self.ip), self.reloadslamwared.__name__)
        self.ssh.Exec("systemctl daemon-reload")
        self.ls.log_print("system", "reload the slamwared success", self.reloadslamwared.__name__)

    def rmstmslog(self):
        self.ls.log_print("system", "remove the log of stms on " + str(self.ip), self.rmstmslog.__name__)
        self.ssh.Exec("if [ -f /home/root/slamware.stms ]; then rm /home/root/slamware.stms fi")
        #| here can using sftp to remove the file
        self.ls.log_print("system", "remove the log of stms success", self.rmstmslog.__name__)

    def getmotor(self):
        self.stopslamwared()
        motor = str(self.ssh.Exec("slamware_base_console -c slamware-core motor"))
        self.startslamwared()
        print motor
        if "Successfully" in motor:
            temp = motor.split(",")[7].split(":")
            left = temp[1].strip().split(" ")[0].split("mm")[0]
            right = temp[2].strip().split("mm")[0]
            result_motor = [left, right]
        else:
            result_motor = False
        return result_motor


if __name__ == "__main__":
    sc = SlamwaredControl()
    sc.getSSH("192.168.11.1", "root", "slamware123")
    left = ""
    right = ""
    print sc.getmotor()