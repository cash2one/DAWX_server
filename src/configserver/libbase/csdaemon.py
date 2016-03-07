#!/bin/env python
#coding=utf-8

# Author: wsh
# Time : 2015-06-10
# 抄袭网上的代码 自己改编
# 读书人的事不能说抄

import sys
import os
import time
import atexit
import string
import signal


"""
    守护进程模块
    --------------

    实现python程序的后台启动，只要重写 **run()** 函数即可。


"""

class Daemon:
    """Daemon 主要是实现程序的后台运行，另外还可以实现日志向另外一个进程传送。

       通过将 stdin， stdout， stderr三个出入输出流进行定向来进行日志的保存
    
    """
    def  __init__(self, pidfile, stdin='/tmp/huihui.log', stdout ='/tmp/huihui.log', stderr = '/tmp/huihui.log' , home_dir='.', umask=022, verbose = 1 ,debug = False  ):
        # 如果需要调试，更改为stdin='/dev/stdin',stdout='/dev/stdout',stderr='/dev/stderr', 以root身份运行
        """init 函数

           参数有如下::
             **pidfile:* pid进程文件
             **stdin:* 输入流的日志记录
             **stdout:* 输入流的日志记录
             **stderr:* 错误流的日志记录
             **home_dir:* 日志的存放目录
             **umask:** 设置权限
             **verbose:** 版本号
             **debug:** 是否开启debug
           
        """
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.home_dir = home_dir
        self.verbose = verbose
        self.umask = umask
        self.daemon_alive = True


    def daemonize(self):
        """
        Do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16

        Arguments:
        - `self`:
        """
        try:
            pid = os.fork()
            if pid > 0:
                print "pid is " + str(pid)
                # 退出主进程
                sys.exit(0)
        except OSError,e:
            sys.stderr.write('Fork#failed: %d (%s)\n'%(e.errno,e.strerror))
            sys.exit(1)

        # Do second fork
        os.chdir(self.home_dir)
        os.setsid()
        os.umask(self.umask)

        # Do second fork
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError,e:
            sys.stderr.write('fork #2 failed: %d(%s)\n'% (e.errno,e.strerror))
            sys.exit(1)

        if sys.platform !='darwin':
            # this block breaks on OS X
            # Redirect standard file descriptirs
            sys.stdout.flush()
            sys.stderr.flush()
            si = file(self.stdin,'a+')
            so = file(self.stdout,'a+')
            if self.stderr:
                se = file(self.stderr,'a+',0)
            else:
                se = so

            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

        def sigtermhandler(signum, frame):
            self.daemon_alive = False
            signal.signal(signal.SIGTERM, sigtermhandler )
            signal.signal(signal.SIGINT, sigtermhandler )

        if self.verbose >= 1:
            print "Started "


        # Write pidfile
        atexit.register(self.delpid)  #make sure pid file is removed if we quit
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n"% pid)


    def delpid(self):
        """ remove the pidfile
        """
        os.remove(self.pidfile)

    def start(self, *args,  **kwargs):
        """
        start the daemon
        """
        if self.verbose >= 1:
            print "starting...."

        # check for a pidfile to see if the daemon alreadby runs
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        except SystemExit:
            pid = None

        if pid :
            message = "pidfile %s alreadby exists. Is it alreadby running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # start the daemon
        self.daemonize()
        self.run(*args, **kwargs)


    def stop(self):
        """
        Stop the daemon
        """

        if self.verbose >= 1:
            print "Stopping...."

        # Get the pid from the pidfile
        pid = self.get_pid()

        if not pid:
            message = "pidfile %s does not exist. Not running?\n"
            sys.stderr.write(message % self.pidfile)

            # Just to be sure. A ValueError might occur if the PID file is
            # empty but does actually exist

            if os.path.exists(self.pidfile):
                print "I will remove the pidfile"
                os.remove(self.pidfile)
                return

        # not an error in a restart
        # try killling the raemon process
        print "pid :::"+ str(pid)
        try:
            i = 0
            while True:
                os.kill(pid,signal.SIGTERM)
                time.sleep(0.2)
                i = i + 1
                if i % 10 == 0:
                    os.kill(pid,signal.SIGHUP)
        except OSError,err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                else:
                    print str(err)
                    sys.exit(1)

        if self.verbose >= 1:
            print "Stopped"


    def restart(self):
        """
        Restart the Daemon
        """
        self.stop()
        self.start()

    def get_pid(self):
        """
        get the pid file and check 
        """
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid =None
        except SystemExit:
            pid = None
        return pid

    def is_running(self):
        """ just check the process is alive
        """
        pid = self.get_pid()
        print(pid)
        return pid and os.path.exists('/proc/%d' % pid)
    

    def run(self, *args, **kwargs):
        """
        You should override this method when you subclass Daemon.
        It will be called after the process has been
        daemonized by start() or restart().
        """
        while True:
            sys.stdout.write('%s:hello world\n' % (time.ctime(),))
            sys.stdout.flush()
            time.sleep(2)

if __name__ == '__main__':
    daemon = Daemon('/tmp/test.pid', stdout='/tmp/huihui.log', stderr='/tmp/huihui.log',stdin='/tmp/huihui.log')
    if len(sys.argv) == 2:  
        if 'start' == sys.argv[1]:  
            daemon.start()  
        elif 'stop' == sys.argv[1]:  
            daemon.stop()  
        elif 'restart' == sys.argv[1]:  
            daemon.restart()  
        else:  
            print 'unknown command'  
            sys.exit(2)  
        sys.exit(0)  
    else:  
        print 'usage: %s start|stop|restart' % sys.argv[0]  
        sys.exit(2)


