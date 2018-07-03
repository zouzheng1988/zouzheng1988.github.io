'''
# tools.py
# using to call tool.exe of sdk
# functions:
    1, call tool.exe
    2, get help 
    3, VirtualWall : add clear get
    4, VirtualTrack : add clear get
    5, Map : add clear get
    6, ...
# author : wei.meng @ 20180412 
# version : 0.0.1
'''

import sys,os,time,json
from datetime import datetime

sys.path.append('../System')
from LogShow import LogShow


class SDKTools(object):
    def __init__(self,ip):
        self.class_name = "SDKTools"
        self.ls = LogShow(self.class_name)
        
        self.ip = ip
        self.getPath()        

    def getPath(self):
        self.localpath = os.path.split(os.path.realpath(__file__))[0]
        self.logexepath = os.path.abspath(os.path.join(self.localpath,"..\\win32tools"))
        self.tool = self.logexepath + "\\zeustoolnew.exe"        
        self.tool_t = self.tool + " -t " + self.ip + " "
        return self.tool

    def __str__(self):
        return self.class_name

    def execute(self,args=[]):
        exerun = self.tool + " -t " + self.ip
        for arg in args:
            exerun = exerun + " " + arg
        os.system(exerun)

    def gethelp(self):
        os.system(self.tool + " -h")

    def addVirtualwall(self,x1,y1,x2,y2):
        exerun = self.tool_t + " 1 " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2)
        self.runcommand(exerun)
        time.sleep(5)

    def clearVirtualwall(self):
        exerun = self.tool_t + " 2 "
        self.runcommand(exerun)
        time.sleep(5)

    def getVirtualwall(self):
        filename = "getVirtualWalls"
        if os.path.exists(filename):
            os.remove(filename)
        exerun = self.tool_t + " 3 "
        self.runcommand(exerun)
        time.sleep(5)

    def addVirtualtrack(self,x1,y1,x2,y2):
        exerun = self.tool_t + " 11 " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2)
        self.runcommand(exerun)
        time.sleep(5)

    def clearVirtualtrack(self):
        exerun = self.tool_t + " 12 "
        self.runcommand(exerun)
        time.sleep(5)

    def getVirtualtrack(self):
        filename = "getVirtualTracks"
        if os.path.exists(filename):
            os.remove(filename)
        exerun = self.tool_t + " 13 "
        self.runcommand(exerun)
        time.sleep(5)

    def getMap(self,mapname):
        exerun = self.tool_t + " 21 " + str(mapname)
        self.runcommand(exerun)
        time.sleep(10)

    def setMap(self,mapname):
        exerun = self.tool_t + " 22 " + str(mapname)
        self.runcommand(exerun)
        time.sleep(15)

    def clearMap(self):
        exerun = self.tool_t + " 23 "
        self.runcommand(exerun)
        time.sleep(5)

    def runcommand(self,command):
        try:
            self.ls.log_print("system", "run command now " + str(command))
            os.system(str(command))
        except Exception,e:
            self.ls.log_print("error", str(e))



