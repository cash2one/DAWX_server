#!/bin/env python
#coding=utf-8


#  利用字典形式来处理函数判断
#  Author : wsh
#  Time: 2015-06-01

from  commands.kaixinqu import kaixinqu
from  commands.hequ import hequ
from commands.tarzone import tarzone
from commands.tarfile  import tarfile
from commands.changeZoneTime import changeZoneTime
from commands.mvzone import mvzone
def usage():
    """
    """
    return [True,"U use help"]

def dataanalyse(data):
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
    
