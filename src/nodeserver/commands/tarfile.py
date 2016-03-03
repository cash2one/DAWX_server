#!/bin/env python
#coding=utf-8

# 打包shell的包装
# Author: wsh
# Time: 2015-06-02

import sys
sys.path.append('commands/libbase')

from  getConfigClient import getres,getresbynum
from  subprores import subprores
from  mod_config import getConfig
from  CSLogging import write_logger


def tarfile(alist):
    print alist
    command = "sh commands/shelltools/tarfile.sh"
    subp = subprores(command)
    if not  subp:
        write_logger('error','changeZoneConf delete error ..............')
        return [False,"changeZoneConf delete ERROR occurred!!!"]
    write_logger('debug','changeZoneConf delete  EXE OK!!!!!!!!!!')


    return [True,"Execution OK"]
