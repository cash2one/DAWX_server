#!/bin/env python
#coding=utf-8

# configserver的客户端
# Author： wsh
# Time: 2015-09-22


"""
    urlres
    -------

    向web服务器发送server状态。

"""
import os,sys
import httplib, urllib
from mod_config import getConfig

webip = getConfig('webserver','webip')
webport = int(getConfig('webserver','webport'))
servername = getConfig('servername','name')

class URLRes(object):
    
    def __init__(self,servername=servername,domain = webip, port = webport):
        self.domain = domain
        self.port = port
        self.httpClient = None
        self.data = None
        self.uri = None
        self.headers = None
        self.servername = "ND" + servername

    def setpostparams(self,level,astr):
        """设置发送的post信息
        """
        adict = {'servername':self.servername,'level':level,'data': astr}
        return urllib.urlencode(adict)

    def seturi(self, domain, port=80):
        """设置发送的服务器域名和端口
        """
        self.domain = domain
        self.port = port

    def setheaders(self):
        """设置头文件
        """
        self.headers = {"Content-type": "application/x-www-form-urlencoded"
                        , "Accept": "text/plain"}
        return self.headers

    def geturi(self):
        """ 获取uri
        """
        return self.domain,self.port


    def connect(self):
        """ 连接服务器，返回句柄
        """
        self.httpClient = httplib.HTTPConnection(self.domain,self.port,timeout=30)
        return self.httpClient

    def send(self,level,astr):
        """向web server 发送post请求
        """
        self.httpClient.request("POST","/chat/getlog.html",self.setpostparams(level,astr),self.setheaders())
        response = self.httpClient.getresponse()

        if response.status == 200 :
            return True
        return False

    def close(self):
        """关闭连接
        """
        self.httpClient.close()

    def run(self,level,astr):
        """ 向web发送实时消息。

        :param level： 日志等级
        :param astr:  日志内容
        """
        tag = None
        self.connect()
        try:
            tag = self.send(level,astr)
        except Exception as e:
            raise e
        finally:
            self.close()
            return tag



"""
try:
    params = urllib.urlencode({'wsh': 'tom', 'age': 22})
    headers = {"Content-type": "application/x-www-form-urlencoded"
               , "Accept": "text/plain"}

    httpClient = httplib.HTTPConnection("localhost", 5000, timeout=30)
    httpClient.request("POST", "/chat/log.html", params, headers)


    response = httpClient.getresponse()
    print response.status
    print response.reason
    print response.read()
    print response.getheaders() 
except Exception, e:
    print e
finally:
    if httpClient:
        httpClient.close()
"""
if __name__ == "__main__":
    aurlres =  urlres()
    aurlres.run('asaa is a test')

