#!/bin/env python
#coding=utf-8

# configserver的客户端
# Author： wsh
# Time: 2015-05-31

import sys

from  libbase.getConfigClient  import getres,getresbynum
from libbase.encrypt import getmd5
from  libbase.mod_config import getConfig
from libbase.CSLogging import write_logger
import time

csip = getConfig('csserver','CSip')
csport = int(getConfig('csserver','CSport'))
ndport=int(getConfig('nodeserver','NDport'))


def getnodeip(dbnum):
    res = getresbynum(dbnum)
    if res:
        res = res.replace("'",'').lstrip('[(').rstrip(')]').split(',')
    else :
        write_logger('error',"CSServer return Num error!!")
        return None
    return res[1].strip()


def check_ip(ipaddr):
        addr=ipaddr.strip().split('.')  #切割IP地址为一个列表
        if len(addr) != 4:  #切割后列表必须有4个参数
            print "check ip address failed!"
            return False
        for i in range(4):
                try:
                        addr[i]=int(addr[i])  #每个参数必须为数字，否则校验失败
                except:
                        print "check ip address failed!"
                        return False

                if addr[i]<=255 and addr[i]>=0:    #每个参数值必须在0-255之间
                        pass
                else:
                        print "check ip address failed!"
                        return False
                i+=1
        else:
                print "check ip address success!"
                return True

def runcmd(*args):
    res = "wrong"
    alist = args

    time.sleep(3)


    # 三种情况
    # 1. 只有一个参数，是发送到CSserver的
    if len(alist) == 1 :
        res = getres(alist[0])
    elif len(alist) ==2 :
        dbip = ''
        if str(alist[0]).isdigit() :
            # 2. 两个参数，且第一个参数是数字(非ip)，需要得到ip
            dbip = getnodeip(int(alist[0]))
        elif check_ip(alist[0]) :
            # 3. 两个参数，且第一个参数为ip。
            dbip=alist[0]
        else :
            res = "ip error"

        if  dbip :
            print dbip
            res = getres(alist[1],host=dbip,port=ndport)
    else:
        pass

    return res

def main():
    alist = sys.argv[1:]
    # 三种情况
    # 1. 只有一个参数，是发送到CSserver的
    if len(alist) == 1 :
        res = getres(alist[0])
    elif len(alist) ==2 :
        if str(alist[0]).isdigit() :
            # 2. 两个参数，且第一个参数是数字(非ip)，需要得到ip
            dbip = getnodeip(int(alist[0]))
            if not dbip :
                print [False, " Num Error"]
                return False
        elif check_ip(alist[0]) :
            # 3. 两个参数，且第一个参数为ip。
            dbip=alist[0]

        res = getres(alist[1],host=dbip,port=7777)
    else:
        res="wrong"

    print res
    

if __name__ == '__main__':
    main()
