#!/bin/env python
#coding=utf-8

# 开新区时间错误更改
# Author: wsh
# Time: 2015-10-10


"""
    更改开区时间

    -----------
    开新区的一个小插曲，和开新区相比，只是做了开新区脚本中更改时间的部分。

    在命令行的实现为::

        telnet > changezonetime dbnum  time

    *dbnum*: 区服号码

    *time*：8位的时间形式，like：20151011


   

"""

import sys
sys.path.append('commands/libbase')



from getConfigClient import getres,getresbynum
from subprores import subprores
from mod_config import getConfig
from CSLogging import write_logger


def changeZoneTime(alist):
    """更改区服时间的操作非常的简单，操作如下::

        1. 参数判断，必须是两个参数
        2. 是否为老区判断(未做)
        3. 更改时间脚本执行

    需要注意的是::

        1. 参数中第一个为 *dbnum* ，第二个为 *time* ，时间参数的格式必须为"20150101"(8位)


    """
    if len(alist) != 2:
        write_logger('error',"len(cmd) error")
        return [False, "len(cmd) error!!"]
    num = int(alist[0])
    time = alist[1]
    if len(time) !=  8:
        write_logger('error',"len(time)(required: 8)  error")
        return [False,"Time error!!,len(time)(required: 8) error"]


    # 1, 进行开区文件copy，重新启动cgi
    command = "sh commands/shelltools/changeZoneTime.sh" + " " +  str(num) +" "+ time
    #command = "echo $PATH"
    subp = subprores(command)
    if not subp:
        write_logger('error',"sh: changeZoneTime.sh, ERROR occurred!!!")
        return [False,"sh: changeZoneTime.sh, ERROR occurred!!!"]

    return [True,"Execution OK"]
    # 更改config服务器的为已经开区



if __name__ == '__main__':
    res = changeZoneTime(['218', '20150418'])

