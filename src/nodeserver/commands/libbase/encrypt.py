#!/bin/env python
#coding=utf-8

# 加密
# Author： wsh
# Time: 2015-06-15

"""
     encrypt
     ----------

     加密程序，目前简单是一个md5加密。

"""


import hashlib,time
from datetime import date
from mod_config import getConfig

entrystr = getConfig('entry','str')

def getmd5():
    """然后一个时间和字符串的md5值。
    """
    amd5str = hashlib.md5(entrystr + str(int(time.time())/86400)).hexdigest()
    return amd5str

if __name__ == '__main__':
    print getmd5()
