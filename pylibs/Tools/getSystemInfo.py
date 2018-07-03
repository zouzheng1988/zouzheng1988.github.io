'''
# get system informations
# version 0.1.0
# 20180108
# M : 20180109 - get pidof slamwared & slamware_agent | get top infos
# M : 20180130 - add run_TopInfo() function 
# M : 20180201 - add split line
# M : 20180206 - add debug and sleep to every step
# M : 20180308 - add QA-465 features : https://jira.slamtec.com/browse/QA-465
'''

import sys,time,os,datetime,json

sys.path.append('../System')
from LogShow import LogShow
from SSH import Ssh
import subprocess
import ctypes

class GetSysInfo(object):
    def __init__(self, ip):
        self.func_name = "GetSysInfo"
        self.ls = LogShow(self.func_name)
        self.ip = ip
        self.user = "root"
        self.password = "slamware123"
        self.ssh = Ssh(self.ip, self.user, self.password)

    def __str__(self, ip):
        return self.func_name
        
    def getTopInfo(self):
        try:
            while True:
                try:
                    self.ssh.Connect()
                    self.data_slamwared = {}
                    tempx_slamwared = self.ssh.Exec_system("pidof slamwared")
                    if len(tempx_slamwared) > 0:
                        self.pidofslamwared = tempx_slamwared[0].replace("\n","")
                    else:
                        continue
                    tempx_agent = self.ssh.Exec_system("pidof slamware_agent")
                    if len(tempx_agent) > 0:
                        self.pidofslamware_agent = tempx_agent[0].replace("\n","")
                    else:
                        continue
                    out = self.ssh.Exec_system("top -n1 | grep " + str(self.pidofslamwared))
                    out_1 = self.ssh.Exec_system("top -n1 | grep " + str(self.pidofslamware_agent))
                    if len(out) > 0:
                        self.slamwared_info = str(out[0]).replace("\n","")
                    else:
                        continue

                    if len(self.slamwared_info ) > 0:
                        self.data_slamwared["slamwared"] = self.slamwared_info.split(" ")
                    else:
                        continue
                    self.data_slamwared["origin_slamwared"] = self.slamwared_info

                    if len(out_1) > 0:                        
                        self.slamware_agent_info = str(out_1[0]).replace("\n","")
                    else:
                        continue
                    if len(self.slamware_agent_info) > 0:                       
                        self.data_slamwared["slamware_agent"] = self.slamware_agent_info.split(" ")
                    else:
                        continue

                    self.data_slamwared["origin_slamware_agent"] = self.slamware_agent_info
                    return self.data_slamwared
                except Exception,e:
                    continue
        except Exception, e:
            self.ls.log_print("error", str(e))

    def printTopInfo(self):
        try:                        
            self.ls.log_print("system", "              [  PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND  ]")
            self.ls.log_print("system", "slamwared      " + self.slamwared_info)
            self.ls.log_print("system", "slamware_agent " + self.slamware_agent_info)
        except Exception,e:
            self.ls.log_print("error", str(e))

    def analysisTopInfo(self):
            slamwaredinfo = """[-PID-PPID-USER-STAT--VSZ-%VSZ-%CPU-COMMAND]\n"""
            flag = 0
            for x in self.data_slamwared["slamwared"]:
                self.ls.log_print("debug", "flag is " + str(flag) + ", x is " + str(x))
                if len(x)==0:
                    continue
                if flag==0 or flag==1 or flag==5 :
                    slamwaredinfo = slamwaredinfo + "-" + x
                if flag==2 or flag==3 or flag==4:
                    slamwaredinfo = slamwaredinfo + "----" + x
                if flag==6 or flag==7:
                    slamwaredinfo = slamwaredinfo + "--" + x
                flag = flag + 1

            slamwaredinfo += "\n"

            flag = 0
            for x in self.data_slamwared["slamware_agent"]:            
                self.ls.log_print("debug", "flag is " + str(flag) + ", x is " + str(x))
                if len(x)==0:
                    continue
                if flag == 0 or flag == 1 or flag == 5 :
                    slamwaredinfo = slamwaredinfo + "-" + x
                if flag == 2 or flag == 3 or flag == 4:
                    slamwaredinfo = slamwaredinfo + "----" + x
                if flag == 6 or flag == 7:
                    slamwaredinfo = slamwaredinfo + "--" + x
                flag = flag + 1
            
            return slamwaredinfo
            
    def run_TopInfo(self):
        try:
            self.ls.log_print("system", "******************************************************************")
            self.getTopInfo()
            self.printTopInfo()
            slamwaredinfo = self.analysisTopInfo()
            self.ls.log_print("system", "******************************************************************")
            return slamwaredinfo
        except Exception, e:
            self.ls.log_print("system", "[ run_TopInfo ]" + str(e))

    def startDiagnosisDebugLog(self):
        try:
            #get log.exe path
            self.ls.log_print("debug", "******")
            self.ls.log_print("system", "start getDiagnosisDebugLog")
            self.localpath = os.path.split(os.path.realpath(__file__))[0]
            self.logexepath = os.path.abspath(os.path.join(self.localpath,"..\\win32tools\\system"))
            self.logexe =  self.logexepath + "\\log.exe"
            #running the exe
            args = [self.ip]
            self.popen = subprocess.Popen(self.logexe + " " + args[0] )            
            self.ls.log_print("debug", "******")
        except Exception, e:
            self.ls.log_print("system", "[ startDiagnosisDebugLog ]" + str(e))

    def stopDiagnosisDebugLog(self):
        try:
            #stop log.exe path
            ctypes.windll.kernel32.TerminateProcess(int(self.popen._handle), -1)
        except Exception, e:
            self.ls.log_print("system", "[ stopDiagnosisDebugLog ]" + str(e))

    def analysisOnlineSlamLog(self):
        try:
            #log line is bellow
            #2018.03.08 16:53:16 [ OnlineSlamLog ] (SYSTEM) Iteration time: 19 ms, Frequency: 52 Hz, Average Frequency: 44 Hz
            if os.path.exists("log/OnlineSlamLog.log"):
                f = open("log/OnlineSlamLog.log", "r")
                for line in f.readlines():
                    if "Average" in line and str(line).strip().endswith("Hz"):
                        tempstr = line.split(" ")
                        if int(tempstr[len(tempstr)-2]) < 20:
                            return line
                return True
            else:
                self.ls.log_print("error", "[ stopDiagnosisDebugLog ] not find onlineslamlog file at log dir")
                return True
        except Exception, e:
            self.ls.log_print("error", "[ stopDiagnosisDebugLog ]" + str(e))

if __name__ == "__main__":
    gsi = GetSysInfo("10.16.131.214")
    while True:
        gsi.getTopInfo()
        gsi.printTopInfo()
        time.sleep(1)