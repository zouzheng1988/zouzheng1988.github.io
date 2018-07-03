'''
# createJson.py
# functions :
    1, write json file
    2, ...
# version 0.0.1
# date 20171016
# author wei.meng
'''

import sys,os,time,json
from LogShow import LogShow

class createJson(object):

    def __init__(self, testname, testresult, test_time_start, test_time_end, test_time_used, test_times_all, test_detail, build_status, error_reason):
        self.ls = LogShow("createJson")
        self.ls.log_print("system", "[createJson] -- start")
        try:
            if testname != None and testname != "" :
                self.testname = testname
            else :
                self.ls.log_print("error", "the testname is None or \'\' !")

            if testresult != None and testresult !="" :
                self.testresult = testresult
            else :
                self.testresult = "fail"

            if test_time_start != None and test_time_start != "" :
                self.test_time_start = test_time_start
            else :
                self.test_time_start = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))

            if test_time_end != None and test_time_end != "" :
                self.test_time_end = test_time_end
            else :
                self.test_time_end = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))

            if test_time_used != None and test_time_used != "" :
                self.test_time_used = test_time_used
            else :
                self.test_time_used = "0s"

            if test_times_all != None and test_times_all != "" and test_times_all != 0 :
                self.test_times_all = 1
            else :
                self.test_times_all = 1

            if build_status != None and build_status != "" :
                self.build_status = build_status
            else :
                self.build_status = "Abort"
            
            if error_reason != None and error_reason != "" :
                self.error_reason = error_reason
            else :
                self.error_reason = "don't know why, see log please!"
                
            self.test_detail = [
                {
                    "test_times" : 1,
                    "test_result" : "failed",
                    "test_time_start" : self.test_time_start,
                    "test_time_end" : self.test_time_end,
                    "test_time_used" : self.test_time_used,
                    "test_log_path" : ".\\log\\",
                    "test_movie_path" : ".\\log\\",
                    "test_report_path" : ".\\log\\"
                }
            ]

        except Exception,e:
            self.ls.log_print("error", "wrong with something " + str(e))

    def writejsonfile(self):
        self.ls.log_print("info", "start write json file !")
        jsoninfo = {
            "testname" : self.testname,
            "testresult" : self.testresult,
            "test_time_start" : self.test_time_start,
            "test_time_end" : self.test_time_end,
            "test_time_used" : self.test_time_used,
            "test_times_all" : self.test_times_all,
            "test_detail" : self.test_detail,
            "build_status" : self.build_status,
            "error_reason" : self.error_reason
        }
        try:
            output = open('testinfo.json', 'wb')
            output.write(json.dumps(jsoninfo))
            output.close()

        except Exception, e:
            self.ls.log_print("error", "wrong with write to the jsonfile " + str(e))
            sys.exit(1)
        self.ls.log_print("info", "write json file success !")


