#!/bin/env python
#coding=utf-8

# configserver的客户端
# Author： wsh
# Time: 2015-05-31


from socket import *
import sys
import time
from  CSLogging import write_logger
from encrypt import getmd5
from mod_config import getConfig

csip = getConfig('csserver','CSip')
csport = int(getConfig('csserver','CSport'))


def getres(astr,host=csip,port=csport):
    """处理并返回结果

    Arguments:
    - `client，sys.argv`:
    """
    time.sleep(0.1)
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
    """获取区号的config配置

    Arguments:
    - `num`:
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
        write_logger("DEBUG","EXE OK!!!!!!!!!!!!!!!")
    else :
        write_logger('error',"CSServer return  None!!")

