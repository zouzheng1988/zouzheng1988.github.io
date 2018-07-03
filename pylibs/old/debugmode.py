#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
# before : pip install requests 
   it is useful to the zeus-edison device to get into debug and simulator mode
   the default config file is /etc/sdp_ref.json
            ssh.Exec("mv /etc/sdp_ref.json /home/root/sdp_ref.json ")
            ssh.Exec("mv /home/root/sdp_ref_simulator.json /etc/sdp_ref.json ")
# author : wei.meng
# date   : 20170301
# ver    : 1.50
# modify : 2017.03.02 - add info of data , change user_pass to self.unlock_info
# modify : 2017.03.03 - change to root mode , delete the simulator mode
# modify : 2017.03.09 - add new flag root 
# modify : 2017.03.17 - add new flag unroot , log , unsimulator -- add new function getlog
# modify : 2017.04.20 - add new function : test the depthcam
# modify : 2017.05.23 - replace 'unroot' by 'unrt' and replace 'unsimulator' by 'unsm' 
# modify : 2017.05.27 - modify the  log get function , to get the logs after rebooting
# modify : 2017.07.21 - modify the test realsense : add put file to remote
# modify : 2017.12.27 - change unlock(root) to local model
# modify : 2018.01.17 - change to 10.16.2.160 , add open diagnosis and close diagnosis
'''

import requests
import json
import sys,os
import time
import traceback,platform
from SSH import Ssh,Sftp
from LogShow import LogShow
from UnlockSN import UnlockSN

class Root(object):

    def __init__(self,ipadd):
        self.ip = ipadd
        self.url_login = 'http://' + self.ip + '/service/system/login'
        self.url_debug = 'http://' + self.ip + '/service/system/admin/challenge'
        self.url_unroot = 'http://' + self.ip + '/service/system/admin/unroot'
        self.url_sn = 'http://' + self.ip + '/service/system/admin/sn'
        self.url_version = "http://" + self.ip + "/service/system/firmware_upgrade/version"
        self.url_diagnosis = "http://" + self.ip + "/service/system/diagnosis"
        self.data_login = {'name':'admin', 'pw':'admin111'}
        self.ssh_user = "root"
        self.ssh_pass = "slamware123"
        self.unlock_info={'ip':'10.16.2.160','user':'token','pass':'admin123'}
        self.data_debug = None
        self.ls = LogShow("Root")


    def Login(self):
        self.ls.log_print("system", "the ip is " + self.ip)
        self.session = requests.Session()
        self.ls.log_print("system", '[Login] session init, ready to login.')
        login = self.session.post(url=self.url_login,data=self.data_login)
        self.ls.log_print("system", '[Login] login successfully')
        return login

    
    def GetSN(self):
        try:
            self.content = self.session.get(self.url_sn).text
            self.sn = json.loads(self.content)["DeviceSN"]
            self.ls.log_print("system", "[getdevicesn] sn is " + self.sn)
            return self.sn
        except:
            self.ls.log_print("system", '[device sn] wrong with get sn')
            
    def GetSN_1(self):
        try:
            self.content = self.session.get(self.url_sn).text
            self.content_1 = json.loads(self.content)
            if self.content_1.has_key("Base(zeus base) SN"):
                self.sn_1 = self.content_1["Base(zeus base) SN"]
            else:
                self.sn_1 = self.content_1["Base(ref base) SN"]
            self.ls.log_print("system", "[getsn] sn is " + self.sn_1 )
            return self.sn_1
        except:
            self.ls.log_print("system", '[sn] wrong with get sn')

    def GetIpMode(self):
        try:
            self.content = self.session.get(self.url_sn).text
            self.ipmode = json.loads(self.content)["MODE : SSID : IP"]
            self.ls.log_print("system", "[getip] ip is " + self.ipmode)
            return self.ipmode
        except:
            self.ls.log_print("system",'[getip] wrong with get sn')
       

    def Getversion(self):
        try:
            self.content = self.session.get(self.url_version).text
            self.version = json.loads(self.content)["FWVERSION"]
            self.ls.log_print("system", self.version)
            return self.version
        except Exception, e:
            self.ls.log_print("error", "[Getversion] exception : " + str(e))


    # cannot get from the web...
    def GetLidarType(self):
        self.content = self.session.get(self.url_sn).text

    def GetFWversions(self):
        try:
            self.ls.log_print("system", "get the fw versions now ..")
            self.content = self.session.get(self.url_version).text
            fwversions = {}
            fwversions = json.loads(self.content)
            return fwversions
        except Exception, e:
            self.ls.log_print("error", "[GetFWversions] exception : " + str(e))

    def GetUnlock(self):
        try:
            ssh = Ssh(self.unlock_info['ip'],self.unlock_info['user'],self.unlock_info['pass'])
            ssh.Connect()
            self.snunlock = ssh.Exec("cd unlock && ./gen_challenge_token.sh " + self.sn)[2]
            ssh.Close()
            self.ls.log_print("system", "[sn-unlock-num] " + self.snunlock)
            self.data_debug = {'cha-token':self.snunlock}
        except Exception,e:
            self.ls.log_print("system",'[sn-unlock] wrong with get sn unlock')
            raise e

    def GetUnlock_local(self):
        try:
            uc = UnlockSN(self.sn)
            self.snunlock = uc.sign()
            self.ls.log_print("system", "[sn-unlock-num] " + self.snunlock)
            self.data_debug = {'cha-token':self.snunlock}
        except Exception,e:
            self.ls.log_print("system",'[sn-unlock] wrong with get sn unlock')
            raise e
    
    def OpenDiagnosis(self):
        try:            
            data_diagnosis = {}
            data_diagnosis["diagnosis"] = "enable"
            self.session.post(url=self.url_diagnosis,data=data_diagnosis)
            self.ls.log_print("system", "[root] successful")
            return True
        except Exception,e:        
            self.ls.log_print("system", '[open diagnosis] wrong with ' + str(e))
            raise e
            return False
            
    def CloseDiagnosis(self):
        try:            
            data_diagnosis = {}
            data_diagnosis["diagnosis"] = "disable"
            self.session.post(url=self.url_diagnosis,data=data_diagnosis)
            self.ls.log_print("system", "[root] successful")
            return True
        except Exception,e:        
            self.ls.log_print("system", '[close diagnosis] wrong with ' + str(e))
            raise e
            return False
            
    def Root(self):
        try:
            self.session.post(url=self.url_debug,data=self.data_debug)
            self.ls.log_print("system", "[root] successful")
            return True
        except:
            self.ls.log_print("system",'[root] wrong with root')
            return False

          
            
    def UnRoot(self):
        try:
            self.session.post(url=self.url_unroot)
            self.ls.log_print("system", "[unroot] successful")
        except:
            self.ls.log_print("system", '[unroot] wrong with the unroot')

    def UploadFile(self):
        try:
            sf = Sftp(self.ip)
            sf.Connect()
            sf.PutFile("..\\testdata\\mapjson\\5f.bmp","/home/root/5f.bmp")
            sf.PutFile("..\\testdata\\mapjson\\sdp_ref_simulator.json","/home/root/sdp_ref_simulator.json")
            sf.Close()
            self.ls.log_print("system", "[upload-file] successful")
        except:
            self.ls.log_print("system", '[upload file] wrong with the it')

    def Simulator(self):
        try:
            ssh = Ssh(self.ip,self.ssh_user,self.ssh_pass)
            ssh.Connect()
            ssh.Exec("mv /etc/sdp_ref_rplidar.json /home/root/sdp_ref.json ")
            ssh.Exec("mv /home/root/sdp_ref_simulator.json /etc/sdp_ref_rplidar.json ")
            ssh.Exec("reboot -n")            
            ssh.Close()
            self.ls.log_print("system", "[Simulator Mode] switch successful")
        except:
            self.ls.log_print("system", '[Simulator Mode]Simulator Mode wrong ')

            
    def TestRealSense(self):
        try:
            ssh = Ssh(self.ip,self.ssh_user,self.ssh_pass)
            ssh.Connect()
            ssh.Exec("echo /usr/bin/slamware_console  depthcam -c tcp status > testrealsense.sh")
            ssh.Exec("chmod a+x testrealsense.sh")
            ssh.Exec("./testrealsense.sh | grep Successfully > realsense.log")
            ssh.Close()
            
            sf = Sftp(self.ip)
            sf.Connect()
            sf.GetFile("/home/root/realsense.log",".\\realsense.log")
            sf.Close()
            self.ls.log_print("system", "[Test Realsense] - successful ")
        except:
            self.ls.log_print("system", "[Test Realsense] - fail to ")
            
            
    def UnSimulator(self):
        try:
            ssh = Ssh(self.ip,self.ssh_user,self.ssh_pass)
            ssh.Connect()
            ssh.Exec("mv /etc/sdp_ref_rplidar.json /home/root/sdp_ref_simulator.json ")
            ssh.Exec("mv /home/root/sdp_ref.json /etc/sdp_ref_rplidar.json ")
            ssh.Exec("reboot -n")            
            ssh.Close()
            self.ls.log_print("system", "[Simulator Mode] switch successful")
        except:
            self.ls.log_print("system", '[UnSimulator] wrong' )
    
    def GetLog(self,logname):
        try:
            ssh = Ssh(self.ip,self.ssh_user,self.ssh_pass)
            '''
            while True:
                try:
                    ssh.Connect()
                    ssh.Exec_noretrun("reboot")
                    print "[getlog] waitting for rebooting to get the log file"

                    break
                except:
                    print "[getlog] wrong with reboot"
                    time.sleep(3)
                    continue
            while True:
                try:
                    ssh.Connect()
                    ssh.Close()
                    print "[getlog] waitting for rebooting to get the log file"
                    break
                except:
                    print "[getlog] waitting for rebooting to get the log file"
                    time.sleep(3)
                    continue
            '''

            ssh.Connect()
            ssh.Exec("journalctl > /home/root/system.log")          
            ssh.Close()
            self.ls.log_print("system", "[getlog] start get log")
            sf = Sftp(self.ip)
            sf.Connect()
            sf.GetFile("/home/root/system.log","log\\"+logname)            
            # sf.GetFile("/home/root/slamware.stms","log\\slamawre.stms")
            sf.Close()
            self.ls.log_print("system", "[getlog] switch successful")
        except:
            self.ls.log_print("system", '[UnSimulator] wrong')
            
            
    def Run(self,flag,logname):
        try:                
            i = 1
            if "root" in flag :
                while True: 
                    self.ls.log_print("system", "try " + "times " + str(i))
                    try:
                        self.Login().raise_for_status() 
                    except:
                        self.ls.log_print("system", "[login] waitting for login successful")
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        self.GetSN() 
                    except:
                        self.ls.log_print("system", "[GetSN] GetSN wrong")
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        self.GetUnlock_local()
                    except:
                        self.ls.log_print("system", "[GetUnlock_local] GetUnlock_local wrong")
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        if self.Root():
                            self.ls.log_print("system", "root ok")
                        else:
                            self.ls.log_print("system", "[Root] Root wrong")
                            time.sleep(10)
                            i = i + 1
                            continue
                    except:
                        self.ls.log_print("system", "[Root] Root wrong")
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        if "log" in flag:
                            self.ls.log_print("system", "--------")
                            self.GetLog(logname)
                        #root.UploadFile() 
                    except:
                        self.ls.log_print("system", "[GetLog] GetLog wrong")
                        time.sleep(10)
                        i = i + 1
                        continue
                        
                    try:
                        if "simulator" in flag:
                            self.ls.log_print("system", "--------")
                            self.UploadFile() 
                        
                    except:
                        self.ls.log_print("system", "[UploadFile] UploadFile wrong")
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        if "simulator" in flag:
                            self.Simulator()
                            self.ls.log_print("system", "--------")
                       
                    except:
                        self.ls.log_print("system", "[Simulator] Simulator wrong")
                        time.sleep(10)
                        i = i + 1
                        continue
                   
                    break
            if "unrt" in flag:
                while True: 
                    self.ls.log_print("system", "try " + "times " + str(i))
                    try:
                        self.Login().raise_for_status() 
                    except:
                        self.ls.log_print("system", "[login] waitting for login successful")
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        self.UnRoot()
                    except:
                        self.ls.log_print("system", "[unroot] waitting for unroot successful")
                        i = i + 1
                        continue
                    break
                    try:
                        self.UnRoot()
                    except:
                        self.ls.log_print("system", "[unroot] waitting for unroot successful")
                        i = i + 1
                        continue
                    break
            if "unsm" in flag :
                while True: 
                    self.ls.log_print("system", "try " + "times " + str(i))
                    try:
                        self.Login().raise_for_status() 
                    except:
                        self.ls.log_print("system", "[login] waitting for login successful")
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        self.UnSimulator()
                    except:
                        self.ls.log_print("system", "[UnSimulator] waitting for UnSimulator successful")
                        i = i + 1
                        continue
                    break
            if "open_diagnosis" in flag:
                while True:
                    self.ls.log_print("system", "try times " + str(i))
                    try:
                        self.Login().raise_for_status()
                    except :
                        self.ls.log_print("system", "[login] waitting for login successful")
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        self.ls.log_print("system", "[open_diagnosis] waitting for open_diagnosis successful")
                        self.OpenDiagnosis()
                        self.ls.log_print("system", "[open_diagnosis] open successful !")
                    except:
                        self.ls.log_print("system", "[open_diagnosis] waitting for open_diagnosis successful")
                        i = i + 1
                        continue
                    break
                    
            if "close_diagnosis" in flag:
                while True:
                    self.ls.log_print("system", "try times " + str(i))
                    try:
                        self.Login().raise_for_status()
                    except :
                        self.ls.log_print("system", "[login] waitting for login successful")
                        time.sleep(10)
                        i = i + 1
                        continue
                    try:
                        self.ls.log_print("system", "[close_diagnosis] waitting for close_diagnosis successful")
                        self.CloseDiagnosis()
                        self.ls.log_print("system", "[close_diagnosis] close successful")
                    except:
                        self.ls.log_print("system", "[close_diagnosis] waitting for close_diagnosis successful")
                        i = i + 1
                        continue
                    break
                    
        except requests.exceptions.ConnectionError:
            self.ls.log_print("error", 'requests.exceptions.ConnectionError' )
            sys.exit(1)
        except requests.exceptions.Timeout:
            self.ls.log_print("error", 'requests.exceptions.Timeout')
            sys.exit(1)
        except requests.exceptions.RequestException:
            self.ls.log_print("error", 'requests error')
            sys.exit(1)
        
if __name__ == "__main__":
    try:
        args = sys.argv
        if len(args) < 3:
            print "[debugmode.py] wrong with the argv"
            
        ipadd = args[1]
        flag = args[2]
        
        root = Root(ipadd)
                    
        i = 1
        if "root" in flag :
            while True: 
                print ("try " + "times " + str(i))
                try:
                    root.Login().raise_for_status() 
                except:
                    print "[login] waitting for login successful"
                    time.sleep(10)
                    i = i + 1
                    continue
                try:
                    root.GetSN() 
                except:
                    print "[GetSN] GetSN wrong"
                    time.sleep(10)
                    i = i + 1
                    continue
                try:
                    root.GetUnlock_local()
                except:
                    print "[GetUnlock_local] GetUnlock_local wrong"
                    time.sleep(10)
                    i = i + 1
                    continue
                try:
                    root.Root()
                    print "root ok"
                except:
                    print "[Root] Root wrong"
                    time.sleep(10)
                    i = i + 1
                    continue
                try:
                    if "log" in flag:
                        print("--------")
                        root.GetLog()
                    #root.UploadFile() 
                except:
                    print "[GetLog] GetLog wrong"
                    time.sleep(10)
                    i = i + 1
                    continue
                    
                try:
                    if "simulator" in flag:
                        print("--------")
                        root.UploadFile() 
                    
                except:
                    print "[UploadFile] UploadFile wrong"
                    time.sleep(10)
                    i = i + 1
                    continue
                try:
                    if "simulator" in flag:
                        root.Simulator()
                        print("--------")
                   
                except:
                    print "[Simulator] Simulator wrong"
                    time.sleep(10)
                    i = i + 1
                    continue
               
                break
        if "unroot" in flag:
            while True: 
                print ("try " + "times " + str(i))
                try:
                    root.Login().raise_for_status() 
                except:
                    print "[login] waitting for login successful"
                    time.sleep(10)
                    i = i + 1
                    continue
                try:
                    root.UnRoot()
                except:
                    print ("[unroot] waitting for unroot successful")
                    i = i + 1
                    continue
                break
                try:
                    root.UnRoot()
                except:
                    print ("[unroot] waitting for unroot successful")
                    i = i + 1
                    continue
                break
        if "unsimulator" in flag :
            while True: 
                print ("try " + "times " + str(i))
                try:
                    root.Login().raise_for_status() 
                except:
                    print "[login] waitting for login successful"
                    time.sleep(10)
                    i = i + 1
                    continue
                try:
                    root.UnSimulator()
                except:
                    print ("[UnSimulator] waitting for UnSimulator successful")
                    i = i + 1
                    continue
                break
                
    except requests.exceptions.ConnectionError:
        print 'requests.exceptions.ConnectionError'
        sys.exit(1)
    except requests.exceptions.Timeout:
        print 'requests.exceptions.Timeout'
        sys.exit(1)
    except requests.exceptions.RequestException:
        print 'requests error'
        sys.exit(1)
    #except:
     #   print 'upload firmware file successfully, wait for updating'
     #   print sys.exc_info()
