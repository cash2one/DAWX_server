#!/bin/bash
# coding=utf-8

# subprocess模块
# author :wsh
# Time: 2015-05-31

"""
    subprocess
    --------------

    调用系统命令
"""


import subprocess

def subprores(command):
    """执行command，返回状态码
    """
    try:
        retcode = subprocess.call(command,shell=True)
        if retcode == 0 :
            print "Execution OK"
            return True
        elif retcode < 0:
            print "Child was terminated by signal", retcode
            return False
        else:
            print "Child returned",retcode
            return False
    except OSError as e:
        print >> sys.stderr,"Execution failed",e
        return False
    
