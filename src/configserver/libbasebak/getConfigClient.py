#!/bin/env python
#coding=utf-8

# configserver的客户端
# Author： wsh
# Time: 2015-05-31


"""
    getConfigClient
    ----------------

    用来连接 **Sockertserver** 包括（ *CSserver* 和 *NDserver* ）。主体函数 **getres**



"""

from socket import *
import sys
import time
from  CSLogging import write_logger
from encrypt import getmd5
from mod_config import getConfig

csip = getConfig('csserver','CSip')
csport = int(getConfig('csserver','CSport'))


def getres(astr,host=csip,port=csport):
    """向 socketserver发送一个 *astr* 。
    server采用密码验证，所以需要线进行密码判断，然后再传送 * astr * 字符串。
    收到服务器传送的数据之后，进行长度验证，如果不正确，重新传送。
    判断成功或者失败次数超出限制之后端开连接，返回结果。



    :param astr: 字符串命令
    :param host: 发送命令的server ip。 默认是给CSserver发送，
    :param port: server port。 默认是CSserver 的port。

    """
    time.sleep(0.2)
    # 1. 参数初始化
    bufsize = 1024
    addr = (host,port)

    # 1. 初始化socket
    client = socket(AF_INET, SOCK_STREAM)
    try:
        client.connect(addr)
    except error,e:
        write_logger('error', 'Connect  CSSERVER ERROR ')
        return None
    # 这个print 必须存在，因为清空recv缓存
    client.recv(bufsize).strip()

    # check password 不能写在函数外部，需要动态动态生成
    password = getmd5()
    client.sendall('%s \n' % password)
    data = client.recv(bufsize)
    if data.find('OK') < 0:
        client.close()
        write_logger('error', "passsword check error")
        return None

    # 2. data 验证
    #data = sys.argv[1:]
    data = astr
    if not data or data == 'exit':
        write_logger('error', "the str you input is wrong")
        client.close()
        return None

    # 3. data 发送和接收
    client.sendall('%s \n'%data)

    data = ''
    # 增加哨兵进行就错判断
    shaobing = 1
    while True :
        while True:
            tmpbuf  = client.recv(bufsize)
            data += tmpbuf
            if 'wshzaiyunweiend' in  tmpbuf or ( len(tmpbuf) < 16 and 'wshzaiyunweiend' in data ):
                break
        alist = data.split('wshzaiyunwei')
        if (len(alist) == 3 )and  (len(alist[1]) == int(alist[0])):
            data = alist[1]
            break
        else:
            client.sendall('%s \n'% "retry")
            data = ''
            shaobing += 1
            if shaobing == 5:
                data = "getConfigClient  Try  5 times!!!!, error"
                write_logger('error', "getConfigClient  Try  5 times!!!!, error")
                break
    client.close()

    # 检查结果是否是error
    if data.find('error') >= 0:
        return None

    return data.strip()

def getresbynum(num):
    """根据 *dbnum* 获取服务器的基本信息
    """
    astr = 'findbydb '+ str(num)
    res = getres(astr)
    return res



if __name__ == '__main__':
    alist = sys.argv[1:]
    command = " ".join(alist)
    res = getres(command)
    print res
#    print len(res)
    if res :
        write_logger("debug","EXE OK!!!!!!!!!!!!!!!")
    else :
        write_logger('debug',"CSServer return  None!!")

