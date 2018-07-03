'''
# LogShow.py
# functions :

# date : 20170811
# version : 0.3
# author : wei.meng
# desc : using to show logstr as same formate.
# m : 20170825 - key -> keys[key]
# m : 20180409 - add save to file define
'''

import time
import os,sys
import logging

class LogShow(object):

    def __init__(self, logflag):
        self.class_name = 'LogShow'
        self.logflag = logflag
        self.log_set_rank()
        #[%(funcName)s] 
        logging.basicConfig(level = logging.INFO,format = '%(asctime)s %(levelname)s [%(name)s] %(message)s')
        self.logger = logging.getLogger(logflag)
         
    def __str__(self):
        return self.class_name

    def log_set_rank(self):
        self.log_rank = {
            "system" : "SYSTEM",
            "debug" : "DEBUG",
            "info" : "INFO", 
            "warn" : "WARN",
            "error" : "ERROR",
            "fatal" : "FATAL"
        }
        self.log_color = {
            "system" : "white",
            "debug" : "yellow",
            "info" : "blue", 
            "warn" : "red",
            "error" : "red",
            "fatal" : "red"
        }
        self.log_level_num = {
            "system" : 5 ,
            "debug"  : 4 ,
            "info"   : 3 ,
            "warn"   : 2 ,
            "error"  : 1 ,
            "fatal"  : 0 ,
        }

    def log_getsystime(self):
        return time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()) )

    # print log with 'rank' 'funcname' 'self.log_flag'
    def log_print(self, rank, log_str, funcname=None):
        if funcname is None:
            self.log_string = self.log_getsystime() + " [ " + self.logflag + " ] (" + self.log_rank[rank] + ") " + str(log_str)
            self.log_str_temp = log_str
            #print self.log_string
        else:
            self.log_string = self.log_getsystime() + " [ " + self.logflag + " ] (" + self.log_rank[rank] + ") [" + str(funcname) + '] ' + str(log_str)
            self.log_str_temp = '[' + str(funcname) + ']' + log_str
            #print self.log_string
        
        if rank == 'system':
            self.logger.info(self.log_str_temp)
        if rank == 'info':
            self.logger.info(self.log_str_temp)
        if rank == 'debug':
            self.logger.debug(self.log_str_temp)
        if rank == 'error':
            self.logger.error(self.log_str_temp)
        if rank == 'fatal':
            self.logger.fatal(self.log_str_temp)
        if rank == 'warn':
            self.logger.warn(self.log_str_temp)

        self.log_save_to_file("./log", self.logflag + '.log')
        self.log_save_to_one_file('./log')

    # save log local/name
    def log_save_to_file(self, local, name):
        try:            
            if not os.path.exists(local):
                os.makedirs(local)
            if not os.path.exists(local + '/' + name):
                f = open(local + '/' + name, 'w')
                f.close()
            flog = open(local + '/' + name, 'a')
            flog.write(self.log_string + '\n')
            flog.close()
        except Exception,e:
            print str(e)
    
    # save to local/log.log
    def log_save_to_one_file(self, local):
        try:            
            if not os.path.exists(local):
                os.makedirs(local)
            if not os.path.exists(local + '/log.log'):
                f = open(local + '/log.log', 'w')
                f.close()
            flog = open(local + '/log.log', 'a')
            flog.write(self.log_string + '\n')
            flog.close()
        except Exception,e:
            print str(e)