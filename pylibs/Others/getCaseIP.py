'''
# getCaseIP.py
# using to get every case's test-device ip
# functions:
    1, get json from file 'testcases.json'
    2, check if the testcase have special test-device ip
    3, ...
# author : wei.meng@20180412
# version : 0.0.1
'''

from __future__ import unicode_literals
import sys,time,os,json
import yaml

sys.path.append("../System")
from LogShow import LogShow

class CheckIP(object):
    def __init__(self):
        self.class_name = "CheckIP"
        self.ls = LogShow(self.class_name)
        self.jsonpath = "../../../testcases/testcases.json"
    
    def __str__(self):
        return self.class_name

    def getjson(self):        
        try:
            f = open(self.jsonpath, "r")
            jsonstr = json.load(f)
            f.close()
            self.jsoninfo = self.byteify(jsonstr)
        except Exception,e:
            self.ls.log_print("error", str(e), self.getjson.__name__) 

    def check(self, key):
        try:
            self.getjson()
            if self.jsoninfo.has_key("testcases"):
                self.ls.log_print("debug", "testcase found!", self.check.__name__)
                if self.jsoninfo["testcases"].has_key(key):
                    self.ls.log_print("debug", key + " found!", self.check.__name__)                
                    if self.jsoninfo["testcases"][key].has_key("ip"):
                        self.ls.log_print("debug", "ip found!", self.check.__name__)
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