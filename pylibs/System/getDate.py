'''
# getDate.py
# using to get date . time . using time
# functions : 
    1, get today's date
    2, 
# author : wei.meng @ 20180412
'''

import os, sys, time, datetime, json, re

from LogShow import LogShow

class getDate(object):

    timestr = '%Y-%m-%d-%H:%M:%S'
    class_name = 'getDate'
    ls = LogShow(class_name)
    #if using python 3.4
    #timestr = '%Y-%m-%d-%H:%M:%S.%f'
    def __init__(self):
        self.class_name = 'getDate'
        self.ls = LogShow(self.class_name)
        self.timestr = '%Y-%m-%d-%H:%M:%S'

    def __str__(self):
        return self.class_name

    @classmethod
    def getdatetoday(cls):
        return time.strftime(cls.timestr, time.localtime(time.time()))
    
    @classmethod
    def getsomedate(cls, dev=0):
        if dev is 0:
            return cls().getdatetoday()
        else:
            today_date = datetime.datetime.now()
            need_date = today_date + datetime.timedelta(days=dev)
            return need_date.strftime(cls.timestr)

    @classmethod
    def getdatefromstr(cls, string):
        if string is not None and isinstance(string, str):
            afterstr = re.compile("[0-9]{4}-(0[0-9]|1[0-2])-([0|1|2][0-9]|3[0-1])-([0|1][1-9]|2[0-3]).[0-5][0-9].[0-5][0-9]")
            if afterstr.match(string):   
                need_date = datetime.datetime.strptime(string, cls.timestr)
                return need_date
            else:
                cls().ls.log_print('warn', string + ' is invalued date-time string')
                return None
    

    
if __name__ == '__main__':
    print getDate.getdatetoday()
    print getDate.getsomedate()
    print getDate.getsomedate(-3)
    print getDate.getdatefromstr('2188-10-26-05:10:95')
