#!/bin/env python
#coding=utf-8

# hequ
# Author: wsh
# Time: 2015-06-18

""" 
    hequ
    -------

    合区程序

    在命令行的实现为::

        telnet > hequ ip=192.168.0.1 dbnumlist

   *ip*： 可以不使用的，如果不使用，则合区到dbnumlist的第一个区

   *dbnumlist*：空格分开，第一个是合区的value。


"""

import sys

sys.path.append('commands/libbase')
from getConfigClient import getres,getresbynum
from subprores import subprores
from mod_config import getConfig
from CSLogging import write_logger



def getIpAndDBnum(alist):
    """ 获得ip和合区的列表。有两种形式::

         1. 给了合区的ip，则直接返回ip和dbnumlist。
         2. 没有给出ip，则获得dbnumlist的第一个区的ip，然后返回。

    这里面的ip为合区到的ip。理论上合区在任何服务器上都可以。

    """
    ipcheck  = str(type(alist[0]))
    if not  alist[0].isdigit() :
        ip = alist[0].split('=')[1]
        dbnumlist=alist[1:]
    else:
        #ip=getresbynum(alist[0]).replace("'",'').lstrip('[(').rstrip(')]').split(',')[1].strip()
        ip = eval(getresbynum(alist[0]))[0][1]
        dbnumlist=alist

    return ip,dbnumlist



def arch_zone(alist):
    """根据合区的区号进行归档，得到ip-numlist 的对应关系，生成字典。
    """
    adict = {}
    for dbnum in alist:
        res = getresbynum(dbnum)
        if res :
            #res = res.replace("'",'').lstrip('[(').rstrip(')]').split(',')
            res = eval(res)[0]
        else :
            write_logger('error',"CSServer return  None!!")
            return [False,"CSServer return Num error!!"]

        ip =  res[1].strip()
        if ip in adict.keys():
            adict[ip] = adict[ip] + [dbnum,]
        else:
            adict[ip] = [dbnum,]

    return  adict


def changezoneipandvalue(alist,localip):
    """合区涉及的数据库更改，主要更改两个部分::

        1. ip更改
        2. value更改

    """
    dbzonenum=alist[0]

    for dbnum in alist:
        command = 'update dbnum='+ str(dbnum) + " ip=" + localip
        getres(command)
        command = 'update dbnum='+ str(dbnum) + " value=" + dbzonenum
        getres(command)
 

def hequ(alist):
    """ 合区的核心程序。
    目前涉及的几个步骤如下::

        1. 获取ip,numlist 并进行归档。
        2. 根据判断ip是否为本地进行分类操作

             * ip为本地ip，停服。
             * ip不是本机ip，则向该ip发送 **tarzone** 命令

        3. CSserver的数据库更改。主要是更改 *ip* 和 *value*
        4. 由于打包过来的文件日志目录缺失，增加日志目录
        5. 合区脚本执行
        6. 本地domai.conf配置增加。在 *第二步* 的时候将在domai.conf中本地的要合区的dbnum进行了删除。

    需要注意的是::
        1. *ip* 并不是必须存在的，如果存在合区到 *ip* 所在服务器上，如果不存在则合区到第一个 *dbnum* 所在的服务器上。

    """
    localip,dbnumlist = getIpAndDBnum(alist)

    for dbnum in dbnumlist:
        res = getresbynum(dbnum)
        print res
        if res :
            #res = res.replace("'",'').lstrip('[(').rstrip(')]').split(',')
            res = eval(res)[0]
        else :
            write_logger('error',"CSServer return  None!!")
            return [False,"CSServer return Num error!!"]

        # tag 用来判断是否是新区
        print res
        tag = int(res[4])
        if tag != 1 :
            write_logger('error',"Not old zone, can't hequ")
            return [False,"Not old zone . can't hequ"]

    zonedict = arch_zone(dbnumlist)
    print zonedict


    exittag = False
    for ip in zonedict.keys():
        if localip != ip :
            astr = "tarzone " + " ".join([str(x) for x in zonedict[ip]])
            write_logger('info', "sh: %s Ok" % astr)
            getres(astr,host=ip, port=1012)
            # 下载解压区服
            command = "sh commands/shelltools/scp.sh  " +  ip
            subp = subprores(command)
            if not subp:
                write_logger('error',"%s ERROR" % command)
                exittag = True
                return [False,"%s  ERROR occurred!!!" % command ]
            write_logger('info',"%s EXE  OK" % command)
        else:
            # 设置iswork=0，并重启cgi
            astr = " ".join([str(x) for  x in zonedict[ip]])
            command = "sh commands/shelltools/changeZoneConf.sh  delete " + astr
            subp = subprores(command)
            if not subp:
                write_logger('error',"%s ERROR" % command)
                exittag = True
                return [False,"changeZoneConf.sh  delete ERROR occurred!!!"]
            write_logger('info',"%s EXE  OK" % command)

    if exittag == True :
        return [False, "Error happened"]
    # 更改所有dbnum的ip为合区ip
    changezoneipandvalue(dbnumlist,localip)
    write_logger('info', "func: changezoneipandvalue happened!!!!")

    # 创建日志文件
    astr = " ".join([str(x) for x in dbnumlist])

    write_logger('debug','createZoneLog.sh start.....................')
    command = "sh commands/shelltools/createZoneLog.sh " + astr
    subp = subprores(command)
    if not subp:
        write_logger('error',"sh: %s ERROR occurred!!!" % command)
        return [False,"createZoneLog.sh  ERROR occurred!!!"]
    write_logger('debug','createZoneLog.sh EXE Ok!!!!!!!!!!!!!')

    # 执行合区脚本
    write_logger('debug',"hequ.sh  start .............")
    command = "sh commands/shelltools/hequ.sh " + astr
    subp = subprores(command)
    if not subp:
        write_logger('error',"sh %s Error occurred!!!" % command)
        return [False,"hequ.sh ERROR occurred!!!"]
    write_logger('debug',"hequ.sh EXE OK!!!!!!!!!!!!!!!")

    # 更改所有区的iswork=1，重启cgi ，over
    write_logger('debug',"changeZoneConf.sh add starting...............")
    command = "sh commands/shelltools/changeZoneConf.sh  add " + astr
    subp = subprores(command)
    if not subp:
        write_logger('error',"sh %s Error occurred!!!" % command)
        return [False,"changeZoneConf.sh add ERROR occurred!!!"]
    write_logger('debug',"changeZoneConf.sh add EXE OK!!!!!!!!!!!!!!!!!!")

    return [True, "hequ OK!!!!"]

if __name__ == '__main__':
    ip,dbnumlist = getIpAndDBnum(["ip=192.168.100.20",1,2,3])
    #ip,dbnumlist = getIpAndDBnum([1,2,3])
    print ip
    print dbnumlist


