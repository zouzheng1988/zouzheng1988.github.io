'''
# checkIP.py
# function :
    1, get json 
    2, 
# date : 20180408
# version : 0.0.1
# author : wei.meng
# check if using the testcase's own ip 
'''

from __future__ import unicode_literals
import sys,time,os,json
import yaml

sys.path.append(".")
from LogShow import LogShow

class CheckIP(object):
    def __init__(self):
        self.func_name = "CheckIP"
        self.ls = LogShow(self.func_name)
        self.jsonpath = "../../../testcases/testcases.json"

    def getjson(self):        
        try:
            f = open(self.jsonpath, "r")
            jsonstr = json.load(f)
            f.close()
            self.jsoninfo = self.byteify(jsonstr)
        except Exception,e:
            self.ls.log_print("error", str(e)) 

    def check(self, key):
        try:
            self.getjson()
            if self.jsoninfo.has_key("testcases"):
                self.ls.log_print("debug", "testcase found!")
                if self.jsoninfo["testcases"].has_key(key):
                    self.ls.log_print("debug", key + " found!")                
                    if self.jsoninfo["testcases"][key].has_key("ip"):
                        self.ls.log_print("debug", "ip found!")
                        if self.jsoninfo["testcases"][key]["ip"] == "default":
                            return True
            
            return False

        except Exception,e:
            self.ls.log_print("error", str(e))
            return False

    def byteify(self,input):
        if isinstance(input, dict):
            return {self.byteify(key): self.byteify(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

if __name__ == "__main__":
    checkip = CheckIP()
    print checkip.check("GoHome Test")