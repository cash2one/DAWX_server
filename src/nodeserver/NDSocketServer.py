#!/bin/env python
#coding=utf-8

import sys,os
# sys.path.append('commands/libbase')

import SocketServer
import socket
from SocketServer import StreamRequestHandler as SRH
import time
from multiprocessing  import Process


# libbase
from commands import dataanalyse
from  CSLogging import write_logger
from  csdaemon import Daemon
from  mod_config import getConfig
from  encrypt  import getmd5
from  check  import check
from initilize import g,initlize
from  urlres import URLRes


basedir = os.path.abspath(os.path.dirname(__file__))
g.path = basedir
g.name = 'NDserver'


host = getConfig('nodeserver','NDip')
port = int(getConfig('nodeserver','NDport'))
addr = (host,port)
mainpid = getConfig('pid','mainpid')
logpid = getConfig('pid','logpid')
logfile = getConfig('log','logfile')
log2file = getConfig('log','log2file')
log2enable=getConfig('log','enablelog')


class Servers(SRH):
    """Sockertserver handler的封装，记住，这个不是socketserver，是request处理的封装。
    """
    def finish(self,*args,**kw):
        """因为存在bug，所以重写了这个函数
        """
        try:
            if not self.wfile.closed:
                self.wfile.flush()
                self.wfile.close()
        except socket.error:
            pass
        self.rfile.close()

    def handle(self):
        """request 请求的处理函数。并作出response。也是我们处理的核心模块
           它经过了如下几个步骤::
             1. 验证密钥是否正确
             2. 函数交给dataanalyse函数进行处理
             3. 请求回应，并校验
             4. 判断回应是否成功
        """
        try:
            msg = 'got connection from ', self.client_address
            write_logger('info',msg)
            self.wfile.write('connection %s:%s at %s  succeed!\n'%(host,port,time.ctime()))

            while True:
                amd5 =  self.rfile.readline().strip()
                amd5str = getmd5()
                write_logger('debug',amd5str)

                if amd5 != amd5str:
                    self.wfile.write('refused!\n')
                    write_logger('debug','CSserver md5 : %s' % amd5str)
                    write_logger('debug', 'Client CSserver: %s'% amd5)
                    write_logger('error',"PassWord refused")
                    break


                self.wfile.write('check OK!\n')
                write_logger('info',"PassWord check OK!")

                ares=''
                while True:
                    res = ''
                    data = self.rfile.readline().strip()
                    if data != "retry" :
                        if data:
                            write_logger('info', "receive command: %s " % str(data))
                            res = dataanalyse.dataanalyse(data)
                        if res:
                            if res[0]:
                                write_logger('info',"command EXEC OK")
                            else:
                                write_logger('error',"command EXEC FAILED")

                            res = res[1]
                            write_logger('debug',"send result: %s" % res)
                        else:
                            res="None"

                    ares = str(len(str(res))) + "wshzaiyunwei" + str(res) + 'wshzaiyunweiend\n'

                    self.wfile.write(ares)
                    self.wfile.flush()

        except IOError, e:
            if e.errno == 32:
                print "IOError, you can ignore it! -----wsh"

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """我们采用了多线程的异步通信： 采用tcp协议
    """
    pass

class daemonserver(Daemon):
    """设置为以daemon方式运行。Hook 了 main()函数
    """
    def run(self,*args, **kwargs):
        """重写了run()
        """
        main()

class daemon2server(Daemon):
    """远端发送日志的进程， Hook 了 pro2()函数
    """
    def run(self,*args,**kwargs):
        """重写了run()
        """
        pro2()

def maininitlize():
    """初始化函数的封装
    
       主要使用来检验启动的必须条件是否满足
    """
    maininitlize()

def main():
    """主函数

       用来进行数据处理和日志记录，以及命令行的debug模式
    """
    write_logger('info','NDServer is starting')
    server = ThreadedTCPServer(addr,Servers)
    try:
        server.serve_forever()
    except KeyboardInterrupt,e:
        write_logger('debug', 'You cancel it!!!!!')

def pro2():
    """网络日志发送程序
    """
    aurlres = URLRes()
    debug =True if log2enable == "True" else False
    if debug:
        while True:
            res =  g.message_recv.recv()
            if aurlres.run(res[0],res[1]):
                write_logger('error',"can't connect webserver",internal=False)






if __name__ == '__main__':
    daemon = daemonserver(mainpid, stdin=logfile, stdout=logfile, stderr=logfile)
    print type(mainpid)
    print type(logpid)
    daemon2 = daemon2server(logpid, stdin=log2file, stdout=log2file, stderr=log2file)
    p1 = Process(target=daemon.start,args=())
    p2 = Process(target=daemon2.start,args=())
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            p1.start()
            p2.start()
            p1.join()
            p2.join()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
            daemon2.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'debug' == sys.argv[1]:
            p1 = Process(target=main,args=())
            p2 = Process(target=pro2,args=())
            p1.start()
            p2.start()
            p1.join()
            p2.join()
        else:
            print 'unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart|debug' % sys.argv[0]
        sys.exit(2)


