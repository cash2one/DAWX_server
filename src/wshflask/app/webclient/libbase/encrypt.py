#!/bin/env python
#coding=utf-8

# configserver的客户端
# Author： wsh
# Time: 2015-06-15

import hashlib,time
from datetime import date
from mod_config import getConfig

entrystr = getConfig('entry','str')
def getmd5():
    amd5str = hashlib.md5(entrystr + str(int(time.time())/86400)).hexdigest()
    return amd5str

if __name__ == '__main__':
    print getmd5()
