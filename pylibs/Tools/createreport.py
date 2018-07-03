#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
# createreport.py
# function :
    1, create Css
    2, create Report
    3, get Device Info
author : mengwei
date : 20170313
version : 2.21
create report for all stage report - with new fuction to create stage report and statis report
modify : 20170427 - add moveandcheck test report creator function
modify : 20170801 - add TP report , add MapTest report , add SonarTest report
modify : 20170811 - change to common lib now
m : 20170825 - key -> keys[key]
m : 20170907 - add new key up down times
'''

import os, time, sys
import cgi,re
import json
import traceback
import shutil

sys.path.append('../System')
sys.path.append('../WebController')

from WebController import WebController
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET
from LogShow import LogShow

reload(sys)
sys.setdefaultencoding( "utf-8")

class Report(object):

    def __init__(self, session=None):
        self.html1 = """<html>
        <head>
        <meta http-equiv="content-type" content="text/html;charset=utf-8">
        <title>"""
        self.html2 = """</title>
        <link rel="stylesheet" type="text/css" href="wcss.css" 
        </head>
        <body>"""
        self.css = """
        body {
            font:normal 100% verdana,arial,helvetica;
            color:#000000;
            background:#FDFFFF;
        }
        table tr td, table tr th {
            font-size: 68%;
        }
        .table-b table td{border:1px solid #F00} 
        table.details tr th{
            font-weight: bold;
            text-align:center;
            background:#E8FFC4;
        }
        table.details tr td{
            background:#D9FFFF;
        }

        table.general tr th{
            font-weight: bold;
            text-align:center;
            background:#4EFEB3;
        }
        table.general tr td{
            background:#FFFFDF;
        }

        p {
            line-height:1.5em;
            margin-top:0.5em; margin-bottom:1.0em;
        }
        h1 {
            margin: 0px 0px 5px; font: 250% verdana,arial,helvetica; text-align:center;
        }
        h2 {
            margin-top: 1em; margin-bottom: 0.5em; font: bold 125% verdana,arial,helvetica; text-align:center;
        }
        h3 {
            margin-bottom: 0.5em; font: bold 115% verdana,arial,helvetica
        }
        h4 {
            margin-bottom: 0.5em; font: bold 100% verdana,arial,helvetica
        }
        h5 {
            margin-bottom: 0.5em; font: bold 100% verdana,arial,helvetica
        }
        h6 {
            margin-bottom: 0.5em; font: bold 100% verdana,arial,helvetica
        }
        .error {
            font-weight:bold; color:red;
        }
        .fail {
            font-weight:bold; color:purple;
        }
        .pass {
            color:black;
        }
        .Properties {
          text-align:right;
        }
        """

        self.html3 = """<h1>Test Report For """
        self.html4 = """</h1>"""
        self.html5 = """<div style="text-indent:3em">
        <br/><br/>
        </div>
        </body>
        </html>"""
        self.report_name = """report.html"""
        self.title_name = ""
        self.reportfile = None
        self.deviceinfo = {}
        self.ls = LogShow("Create Report")
        self.session = session
        


    def createCSS(self):
        self.tCss = open(".\\report\\wcss.css" , 'wb')
        self.tCss.write(self.css)
        self.tCss.close()

    def createReport(self):
        self.title_name = self.test_json["testname"]
        self.reportfile = open(".\\report\\"+ self.report_name , 'wb')
        self.reportfile.write( self.html1)
        self.reportfile.write( self.title_name + " TEST REPORT")
        self.reportfile.write( self.html2)
        self.reportfile.write( self.html3)
        self.reportfile.write( self.title_name)
        self.reportfile.write( self.html4)

    def getDeviceInfo(self,ipadd):
        root = WebController(ipadd, self.session)
        while True:
            try:
                self.deviceinfo["Device S/N"] = root.getDeviceSN() 
                self.deviceinfo["S/N"] = root.getBaseSN()
                self.deviceinfo["Ip address"] = root.getIPMode()
                self.deviceinfo["FirmWare version"] = root.getVersion()
                break
            except Exception,e:
                self.ls.log_print("system", str(traceback.print_exc()))
                time.sleep(5)
                self.getDeviceInfo()
        # i = 1
        # while True: 
        #     self.ls.log_print ("system", "try " + "times " + str(i))
        #     try:
        #         root.Login().raise_for_status()
        #     except:
        #         self.ls.log_print ("system", "[login] waitting for login successfully")
        #         time.sleep(10)
        #         i = i + 1
        #         continue
        #     try:
        #         self.deviceinfo["Device S/N"] = root.GetSN() 
        #         self.deviceinfo["S/N"] = root.GetSN_1()
        #         self.deviceinfo["Ip address"] = root.GetIpMode()
        #     except:
        #         self.ls.log_print ("system", "[GetSN] GetSN wrong")
        #         time.sleep(10)
        #         i = i + 1
        #         continue
        #     try:
        #         self.deviceinfo["FirmWare version"] = root.Getversion()
        #     except:
        #         self.ls.log_print ("system", "[getversion] getversion wrong")
        #         time.sleep(10)
        #         i = i + 1
        #         continue
                    
        #     break

    def endReport(self):
        self.reportfile.write( self.html5)
        self.reportfile.close()

    def addDeviceInfo(self):
        self.reportfile.write("<div><br/></div><h2>Device Info</h2>\n")
        self.reportfile.write("<table class=\"general\" align=\"center\" style=\"text-align:center\" border=\"0\" cellpadding=\"5\" cellspacing=\"3\" width=\"70%\">\n")
        self.reportfile.write("<tr><th width=\"15%\">Name</th><th width=\"20%\">Value</th><th width=\"15%\">Name</th><th width=\"20%\">Value</th></tr>\n")
        self.reportfile.write("<tr><td>FirmWare version </td> <td>" + str(self.deviceinfo["FirmWare version"]) + "</td><td>Device S/N </td> <td>" + str(self.deviceinfo["Device S/N"]) + "</td></tr>\n")
        self.reportfile.write("<tr><td>S/N </td> <td>" + str(self.deviceinfo["S/N"]) + "</td><td>Ip address </td> <td>" + str(self.deviceinfo["Ip address"]) + "</td><tr>")
        #self.reportfile.write("<tr><td>Ip address </td> <td>" + deviceinfo["Ip address"] + "</td><td>Device S/N </td> <td>" + deviceinfo["Device S/N"] + "</td><tr>")
        self.reportfile.write("</table>")

    def readTestJson(self):
        testinfo = open("testinfo.json","r")
        self.test_json = json.load(testinfo)
        self.infos = ["testname", "testresult", "test_time_start", "test_time_end", "test_time_used", "test_times_all", "test_detail"]
        self.testname = self.test_json["testname"]

    def create_statics_table(self):
        self.reportfile.write("<div><br/></div><h2> " + self.test_json["testname"] + "</h2>\n")
        self.reportfile.write("<table class=\"general\" style=\"text-align:center\"align=\"center\" cellpadding=\"5\" cellspacing=\"2\" width=\"70%\">\n")
        self.reportfile.write("<tr><th>Name</th><th>Start</th><th>End</th><th>Spend</th><th>Result</th><th>TestCount</th></tr>\n")
        self.reportfile.write('<tr><td>' + self.test_json["testname"] + '</td><td>' + self.test_json["test_time_start"] + 
            '</td><td>' + self.test_json["test_time_end"] + '</td><td>' + self.test_json["test_time_used"] + '</td><td>' +
            self.test_json["testresult"] + '</td><td>' + str(self.test_json["test_times_all"]) + '</td></tr>\n')
        self.reportfile.write("</table>")

    def create_detail_table(self):
        i = 1
        for detail in self.test_json["test_detail"] :
            if self.test_json["test_times_all"] == 1:
                self.reportfile.write("<h2> Details </h2>\n")
            else:
                self.reportfile.write("<h2> Test " + str(i) + " Detail </h2>\n")
            i = i + 1
            self.reportfile.write("<table class=\"general\" style=\"text-align:left\" align=\"center\" cellpadding=\"1\" cellspacing=\"1\" width=\"70%\"\n")
            td_str = ""
            th_str = "<tr><th>Name</th><th>Vaule</th></tr>\n"
            allkeys = sorted(detail.keys())
            for th in allkeys:
                if self.findurlpath(th):
                    td_str = td_str + "<tr><td>" + self.keystoname(str(th)) + "</td><td><a href=\"" + str(detail[th]) + "\">" + str(detail[th]) + "</a></td></tr>\n"
                else:
                    if "\n" in str(detail[th]):
                        endstrs = str(detail[th]).replace("\n","<br>")
                        td_str = td_str + "<tr><td>" + self.keystoname(str(th)) + "</td><td>" + endstrs + "</td></tr>\n"
                    else:
                        td_str = td_str + "<tr><td>" + self.keystoname(str(th)) + "</td><td>" + str(detail[th]) + "</td></tr>\n"
            self.reportfile.write(th_str)
            self.reportfile.write(td_str)
            self.reportfile.write("</table>")

    def findurlpath(self,value):
        if "path" in value or "url" in value:
            return True
        else :
            return False

    def keystoname(self,key):
        keys = {        
            "a" : "A",
            "after":"After",
            "b" : "B",
            "before":"Before",
            "begin":"Begin",
            "break":"Break",
            "c":"C",
            "can":"Can",
            "case":"Case",
            "class":"Class",
            "center":"Center",
            "create":"Create",
            "current":"Current",
            "d":"D",
            "do":"Do",
            "down" : "Down",
            "e":"E",
            "end":"End",
            "f":"F",
            "g":"G",
            "h":"H",
            "i":"I",
            "j":"J",
            "k":"K",
            "l":"L",
            "log":"Log",
            "movie":"Video",
            "path":"Path",
            "point":"Point",
            "points":"Points",
            "report":"Report",
            "result":"Result",
            "stop":"Stop",
            "start":"Start",
            "test":"Test",
            "time":"Time",
            "times":"Times",
            "used":"Used",
            "url":"Url",
            "up":"Up",
            "video":"Video",
            "version":"Version"
            }
        if not "_" in key:
            self.ls.log_print("debug", "not include _ ,so key is key")
            if key in keys.keys():
                return keys[key]
            return key
        else:
            key_return = ""
            allkeys = key.split("_")
            for every_key in allkeys:
                if every_key in keys.keys():
                    key_return = key_return + " " + keys[every_key]
                else :
                    key_return = key_return + " " + every_key
            return key_return

    def run(self,ip):
        self.readTestJson()
        self.createCSS()
        self.createReport()
        self.createReport()
        self.getDeviceInfo(ip)
        self.addDeviceInfo()
        self.create_statics_table()
        self.create_detail_table()
        self.endReport()

if __name__ == "__main__":
    #deviceinfo = {"FirmWare version":"zeus_edison.2.2.1_rtm.20170308.bin","Device S/N":"D58F4024E0EDF790D4E9F2F9075483E4","Ip address":"192.168.11.1","S/N":" C47ADDC6F19575BD90A14AC5"}
      
    report = Report()
    report.run("192.168.11.1")