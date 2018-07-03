'''
# date : 20180327
# version : 0.0.1
# author : wei.meng
# using for formate date time out put in all framework
'''

import sys,time,os

def showinfos(func):
    def inner():
        print "--------------------"
        return func()
    return inner


class Others(object):
    def __init__(self):
        self.test_data = "10000"

    @showinfos
    def test(self):
        print "helloworld"

@showinfos
def test():
    print "helloworld"

if __name__ == "__main__":
    test()
    o = Others()
    o.test()