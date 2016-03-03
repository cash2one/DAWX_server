#!/bin/env python
#coding=utf-8

# 开新区的基本操作
# Author: wsh
# Time: 2015-05-31


"""
    kaixinqu
    --------

    开新区程序。

    在命令行的实现为::

        telnet > kaixinqu dbnum  time

    *dbnum*: 区服号码

    *time*：8位的时间形式，like：20151011


"""

import sys
sys.path.append('commands/libbase')



from getConfigClient import getres,getresbynum
from subprores import subprores
from mod_config import getConfig
from CSLogging import write_logger



def kaixinqu(alist):
    """开新区程序的操作非常的简单，操作如下::

        1. 参数判断，必须是两个参数
        2. 是否为新区判断
        3. 开区脚本执行

    需要注意的是::

        1. 参数中第一个为 *dbnum* ，第二个为 *time* ，时间参数的格式必须为"20150101"(8位)


    """
    # 因为只有一个正确结果，所以只需要删除两边的'[('和')]'
    #res = getres("findbydb " + str(num)).lstrip('[(').rstrip(')]').split(',')
    # 20151126 追加： 可以使用eval函数进行处理

    if len(alist) != 2:
        write_logger('error',"len(cmd) error")
        return [False, "len(cmd) error!!"]
    num = int(alist[0])
    time = alist[1]
    if len(time) !=  8:
        write_logger('error',"len(time)(required: 8)  error")
        return [False,"Time error!!,len(time)(required: 8) error"]


    res = getresbynum(num)
    print res
    if res :
        res = eval(res)[0]
    else :
        write_logger('error',"CSServer return  None!!")
        return [False,"CSServer return Num error!!"]

    # tag 用来判断是否是新区
    print res
    tag = int(res[4])
    if tag != 0 :
        write_logger('error',"Not new zone")
        return [False,"Not new zone"]



    # 2, 进行开区文件copy，重新启动cgi
    command = "sh commands/shelltools/CreateNewZone.sh" + " " +  str(num) +" "+ time
    #command = "echo $PATH"
    subp = subprores(command)
    if not subp:
        write_logger('error',"sh: CreateNewZone.sh, ERROR occurred!!!")
        return [False,"sh: CreateNewZone.sh, ERROR occurred!!!"]

    return [True,"Execution OK"]
    # 更改config服务器的为已经开区



if __name__ == '__main__':
    res = kaixinqu(['218', '20150418'])



