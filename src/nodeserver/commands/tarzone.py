#!/bin/env python
#coding=utf-8

# 打包shell的包装
# Author: wsh
# Time: 2015-06-02


"""
  tarzone
  -------

   打包区服

"""

import sys
sys.path.append('commands/libbase')

from  getConfigClient import getres,getresbynum
from  subprores import subprores
from  mod_config import getConfig
from  CSLogging import write_logger



def tarzone(alist):
    """本地存在的alist进行压缩。主要的操作步骤::

        1. 停止要压缩的区服服务。
        2. 压缩区服。


    """
    numstr = " ".join([str(x) for x in alist])

    # 1. 修改配置
    write_logger('debug','changeZoneConf delete starting..............')
    command = "sh commands/shelltools/changeZoneConf.sh  delete " + numstr
    subp = subprores(command)
    if not  subp:
        write_logger('error','changeZoneConf delete error ..............')
        return [False,"changeZoneConf delete ERROR occurred!!!"]
    write_logger('debug','changeZoneConf delete  EXE OK!!!!!!!!!!')

    # 2. 执行压缩命令
    write_logger('debug', 'tarzone.sh starting...............')
    command = "sh commands/shelltools/tarzone.sh  " + numstr
    subp = subprores(command)
    if not subp:
        write_logger('error','tarzone.sh   error ..............')
        return [False,"tarzone.sh  ERROR occurred!!!"]
    write_logger('debug','tarzone.sh EXE OK!!!!!!!!!!')

    return [True,"Execution OK"]

if __name__ == '__main__':
    tarzone(455)

