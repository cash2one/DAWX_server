#!/bin/env python
#coding=utf-8



import sys,os


import SocketServer
import socket
from SocketServer import StreamRequestHandler as SRH
import time
import dataanalyse
from multiprocessing  import Process



# libbase
from  CSLogging  import write_logger
from csdaemon import Daemon
from mod_config import getConfig
from encrypt import getmd5
from check import check
from initilize import g,initlize
from  urlres import URLRes

basedir = os.path.abspath(os.path.dirname(__file__))
g.path = basedir
g.name = 'CSserver'
initlize()




host = getConfig('csserver','CSip')
port = int(getConfig('csserver','CSport'))
addr = (host,port)
mainpid = getConfig('pid','mainpid')
logpid = getConfig('pid','logpid')
logfile = getConfig('log','logfile')
log2file = getConfig('log','log2file')
log2enable=getConfig('log','enablelog')


class Servers(SRH):
    #Don't call the base class finish() method as it does the above
    #return SocketServer.StreamRequestHandler.finish(self)
    def finish(self,*args,**kw):
        try:
            if not self.wfile.closed:
                self.wfile.flush()
                self.wfile.close()
        except socket.error:
            pass
        self.rfile.close()

    def handle(self):
        try:
            msg = 'got connection from ', self.client_address
            write_logger('info', msg)
            self.wfile.write('connection %s:%s at %s  succeed!\n'%(host,port,time.ctime()))
            while True:
                amd5 = self.rfile.readline().strip()
                amd5str=getmd5()


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
                            write_logger('warning', "receive command: %s " % str(data))
                            res = dataanalyse.dataanalyse(data)
                        if res :
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
            pass


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # 异步通信
    pass

class daemonserver(Daemon):

    # 重写run方法
    def run(self,*args, **kwargs):
        main()


class daemon2server(Daemon):
    def run(self,*args,**kwargs):
        pro2()

def main():

    if not check():
        sys.exit(100)
    write_logger('info','CSServer  Check OK')
    write_logger('info','CSServer starts')
    server = ThreadedTCPServer(addr,Servers)
    try:
        server.serve_forever()
    except KeyboardInterrupt,e:
        write_logger('debug', 'You cancel it!!!!!')

def pro2():
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


