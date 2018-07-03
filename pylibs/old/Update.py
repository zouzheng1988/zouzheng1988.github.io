#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
# version : v1.23
# authore : wei.meng
# date    : 20170304
# modify  : 20170503 - add update_new and runupdate_new function at the new slamware version 2.4.0_dev
# modify  : 20170518 - /service/system/system_upgrade is the new action url.
# modify  : 20170605 - bug fix , but not work.
# modify  : 20170621 - add new version check , if version >= 2.4 , using the url _ new
# bugfix  : 20170731 | the Update_New is wrong , fix it to the Update_New 
# modify  : 20180201 - add recheck in function checkversionurl...

####
#   ip - slamware ip
#   url_login - login action url
#   url_update - update action url of version 2.3.x and before
#   url_update_new - updateaction url of version 2.4.x and new
####
'''


import requests
import json
import sys,os
import time
import subprocess,traceback,platform
from LogShow import LogShow
from datetime import datetime

class Update(object):

    def __init__(self,ipadd,fm_path):
        self.ip = ipadd
        self.url_login = 'http://' + self.ip + '/service/system/login'
        self.url_update = 'http://' + self.ip + '/service/system/firmware_upgrade/full_update'
        self.url_status = 'http://' + self.ip + '/service/system/task/status'
        self.url_update_new = 'http://' + self.ip + '/service/system/system_upgrade'
        self.url_restore = 'http://' + self.ip + '/service/system/restore'
        self.firmware_path = fm_path
        self.data_login = {'name':'admin', 'pw':'admin111'}
        self.ls = LogShow("Update")

    # Login the slamware web Administrator with 'admin' and 'admin111'
    def Login(self):
        self.session = requests.Session()
        self.ls.log_print("system", '[login] session init, ready to login' )
        login = self.session.post(url=self.url_login,data=self.data_login)
        self.ls.log_print("system",  '[login] ok')
        return login

    # Update : using file upload the firmware and run it
    def Update(self):
        try:
            files = {'file': open(self.firmware_path, 'rb')}
            self.ls.log_print("system",  '[update] load firmware file successfully, ready to upload firmware file')
            startupdate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            self.ls.log_print("system",  '[ start time ] ' + str(startupdate) )
            self.session.post(url=self.url_update,files=files)
            self.the_real_start = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            self.time_use_1 = datetime.now()
            self.ls.log_print("system", '[update] wait for update [240 s]')
            time.sleep(240)
        except Exception,e:
            if "BadStatusLine" in str(e):

                self.the_real_start = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                self.time_use_1 = datetime.now()
                self.ls.log_print("system",  "[update] <exception> " + str(e) )  
                time.sleep(240)        
            else:
                self.ls.log_print("system",  "[update] <error> " + str(e))
                time.sleep(10)
                self.ls.log_print("system",  "[update] try again ...")
                self.Update()

    def checkversionurl(self,currentversion):
        versioninfo = ["2.4","2.5","2.6","2.7","2.8","2.9","3.0","3.1","3.2","3.3","3.4","3.5","3.6","3.7","3.8","3.9","4.0","4.1"]
        versioninfo_not = ["2.1","2.2","2.3"]
        newback = False
        for f in versioninfo:
            self.ls.log_print("system",  "[update]-[check current] " + f)
            if f in currentversion:
                newback = True
                return True
        if not newback:
            for f in versioninfo_not:
                self.ls.log_print("system", "[update]-[recheck current] " + f)
                if f in currentversion:
                    newback = False
                    return newback
            newback = True
        return newback

    # do not work fine , when "bad line" issue coming , the expect always do the failed job .
    def Update_1(self):
        while True:
            try:
                files = {'file': open(self.firmware_path, 'rb')}
                self.ls.log_print("system",  '[update] load firmware file successfully, ready to upload firmware file')
                startupdate = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
                self.ls.log_print("system",  '[ start time ] ' + str(startupdate) )
                self.session.post(url=self.url_update,files=files)
                self.ls.log_print("system",  ('[update] wait for update [240 s]'))
                time.sleep(240)
                break
            except Exception,e:
                self.ls.log_print("system",  "[update] <error> " + str(e))
                time.sleep(2)
                continue
            except:
                self.ls.log_print("system",  "[update] <error> wrong with update")
                time.sleep(2)
                continue


    # using for the new version check , 2.4.0_dev and higher would be work fine
    def Update_New(self):
        try:
            files = {'file':open(self.firmware_path,'rb')}
            self.ls.log_print("system",  '[update_new] load the firmware file ')
            startupdate = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
            self.ls.log_print("system",  '[update_new - start time] ' + str(startupdate))
            self.session.post(url=self.url_update_new,files=files)
            self.the_real_start = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
            self.time_use_1 = datetime.now()
            self.ls.log_print("debug",  '[update_new] upload ok , start update now ...')
            self.ls.log_print("system", '[update_new] wait for update [240 s]')
            time.sleep(240)
        except Exception,e:
            if "BadStatusLine" in str(e):                
                self.the_real_start = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
                self.time_use_1 = datetime.now()
                self.ls.log_print("system",  "[update_new] <exception> " + str(e)  )
                self.ls.log_print("system", '[update_new] wait for update [240 s]')
                time.sleep(240)        
            else:
                self.ls.log_print("error",  "[update_new] <error> " + str(e))
                time.sleep(10)
                self.ls.log_print("system",  "[update_new] try again ...")
                self.Update_New()
        
    # try to fix some bad line issue , but not work fine ,would fix it on new deal.
    def Update_New_1(self):
        while True:
            try:
                files = {'file':open(self.firmware_path,'rb')}
                self.ls.log_print("system",  '[update_new] load the firmware file ')
                startupdate = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
                self.ls.log_print("system",  '[update_new - start time] ' + str(startupdate))
                self.session.post(url=self.url_update_new,files=files)
                self.ls.log_print("system", '[update_new] wait for update [240 s]')
                time.sleep(240)
                break
            except Exception,e:
                self.ls.log_print("system",  "[Update-new] <error> wrong with " + str(e))
                time.sleep(2)
                continue
            except:
                self.ls.log_print("system",  "[Update-new] <error> wrong with update" )
                time.sleep(2)
                continue
    
    def GetResult(self):
        while True:
            if self.Ping():
                self.ls.log_print("system", "[ping] ok")
            else:
                self.ls.log_print("system", "[ping] waitting for update complete")
                time.sleep(30)
                continue
            try:
                self.Login().raise_for_status() 
            except:
                self.ls.log_print("system",  "[login] waitting for update complete")
                time.sleep(10)
                continue
            try:
                req = self.session.get(url=self.url_status)
                req.raise_for_status() 
            except :
                self.ls.log_print("system",  "[update] waitting for update complete")
                time.sleep(10)
                continue
            ### first of all , using the web info to judge the update complete or not ,
            ### but now ,sdk connect and version info is the double check
            # req_json = json.loads(req.text)
            # if req_json['message'] == 'Idle':
                # endupdate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                # print '[ end time ] ' + str(endupdate) 
                # print 'update successfully'
                # break
            os.system("sdkconnect.exe " + self.ip)
            file = open("connect.result","r")
            f = file.readline()
            file.close()
            
            if "successful" in f:
                self.ls.log_print("system", "[sdk-connect] core startup successful")
                break
            else :
                time.sleep(30)
                    
                
    def Ping(self):
        cmd = 'ping -n %d %s'%(1,self.ip)
        try:
            p = subprocess.Popen(args=cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (stdoutput,erroutput) = p.communicate()
        except Exception, e:
            traceback.print_exc()
        return stdoutput.find('TTL')>=0        

    def RunUpdate(self):
        try:
            i = 1
            while True: 
                self.ls.log_print("system", "[update] try " + "times " + str(i))
                if self.Ping():
                    self.ls.log_print("system", "[ping] ok")
                else:
                    self.ls.log_print("system", "[ping] waitting for network online")
                    time.sleep(30)
                    i = i + 1
                    continue
                try:
                    self.Login().raise_for_status() 
                except:
                    self.ls.log_print("system", "[login] waitting for login successfully")
                    time.sleep(10)
                    i = i + 1
                    continue
                break

            self.Update()
            self.GetResult()
            update_time = {}
            update_time["time_use_1"] = self.time_use_1
            update_time["test_time_start"] = self.the_real_start
            return update_time

        except requests.exceptions.ConnectionError:
            self.ls.log_print("system",  'requests.exceptions.ConnectionError')
            sys.exit(1)
        except requests.exceptions.Timeout:
            self.ls.log_print("system",  'requests.exceptions.Timeout')
            sys.exit(1)
        except requests.exceptions.RequestException:
            self.ls.log_print("system",  'requests error')
            sys.exit(1)


            
    def RunUpdate_New(self):
        try:
            i = 1
            while True:
                self.ls.log_print("system", "[update_new] try times " + str(i))
                if self.Ping():
                    self.ls.log_print("system", "[update_new][ping] ok")
                else :
                    self.ls.log_print("system", "[update_new][ping] waiting for network online")
                    time.sleep(30)
                    i = i + 1
                    continue
                try:
                    self.Login().raise_for_status()
                except:
                    self.ls.log_print("system", "[update_new][login] waitting for login successfully")
                    time.sleep(10)
                    i = i + 1
                    continue
                break   

            self.Update_New()
            self.GetResult()
            update_time = {}
            update_time["time_use_1"] = self.time_use_1
            update_time["test_time_start"] = self.the_real_start
            return update_time
        
        

                
        
        except requests.exceptions.ConnectionError:
            self.ls.log_print("system", 'requests.exceptions.ConnectionError')
            sys.exit(1)
        except requests.exceptions.Timeout:
            self.ls.log_print("system", 'requests.exceptions.Timeout')
            sys.exit(1)
        except requests.exceptions.RequestException:
            self.ls.log_print("system", 'requests error')
            sys.exit(1)
                    
                
    #except:
     #   print 'upload firmware file successfully, wait for updating'
     #   print sys.exc_info()
