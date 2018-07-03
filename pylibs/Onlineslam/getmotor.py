# encoding='utf-8'

'''
# getmotor.py
# using to get motor
# function :
    1, slamware_base_console -c slamware-core motor to get motor
# date : 20180514
# version : 0.1
# author : wei.meng
'''
import os,time,sys
from datetime import datetime

sys.path.append('../System')

from LogShow import LogShow
from SSH import Ssh
from Sftp import Sftp
from slamwaredControl import SlamwaredControl

class getMotor(object):
    def __init__(self):
        self.class_name = "getMotor"
        self.ls = LogShow(self.class_name)


    def __str__(self):
        return self.class_name

    