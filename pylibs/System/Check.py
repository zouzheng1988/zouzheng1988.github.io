'''
# Check.py
# using to check all things
# functions:
    1, check ip is ok

'''

import re
import os, sys, time, datetime, json

class Check(object):

    def __init__(self):
        self.class_name = 'Check'
    
    def __str__(self):
        return self.class_name

    @staticmethod
    def checkIP(ipadd):
        if isinstance(ipadd, str):
            ip = ipadd
        else:
            ip = str(ipadd)

        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip):
            return True
        else:
            return False


if __name__ == '__main__':
    check = Check()
    print check.checkIP('11.16.1310.129')
    print Check.checkIP('10.16.130.111')