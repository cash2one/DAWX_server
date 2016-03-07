#!/bin/env python
#coding=utf-8


#  利用字典形式来处理函数判断
#  Author : wsh
#  Time: 2015-06-01

from  kaixinqu import kaixinqu
from  hequ import hequ
from tarzone import tarzone
from tarfile  import tarfile
from changeZoneTime import changeZoneTime
from mvzone import mvzone


"""
    数据处理 
    -----------

    函数和命令的映射程序


"""


def usage():
    """目前可以使用的命令有如下几个::
         1. kaixinqu
         2. tarzone
         3. tarfile
         4. hequ
         5. changgezonetime
         6. mvzone 
    """
    return [True,"U use help"]

def dataanalyse(data):
    """数据处理程序，进行了一些基本的判断和命令与函数的对应

      *data:* 后端接收的命令
    """
    dictname = {'kaixinqu':kaixinqu,
                'tarzone': tarzone,
                'tarfile': tarfile,
                'hequ': hequ,
                'changezonetime':changeZoneTime,
                'mvzone': mvzone
                }
    alist = data.split()
    if not alist:
        return [False,'No command, You should input right command']
    elif alist[0] != 'help' and len(alist) < 2:
        return [False, "command error, You should input right command!! "]

    handlecmd = alist[0]
    if handlecmd in dictname.keys():
        return dictname[handlecmd](alist[1:])
    elif handlecmd == 'help':
        return usage()
    else:
        return [False , "You should input right command!!"]

if __name__ == '__main__':
    res= dataanalyse('help')
    print res[1]
    
