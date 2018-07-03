'''
# date : 20180329
# core.py
'''


import os, time, datetime, sys

class CoreAppException(BaseException):
    def __new__(self):
        be = BaseException()
        return be

class CoreApp(object):

    def __init__(self):
        pass

    def __str__(self):
        return "CoreApp"

    def __len__(self):
        return 1

    def __bool__(self):
        return True

    def run(self):
        cae = CoreAppException()
        return cae
        pass



if __name__ == "__main__":
    try:
        coreApp = CoreApp()
        coreApp.run()
        #print str(coreApp)
    except CoreAppException,e:
        print "====" + str(e)
