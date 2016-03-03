#encoding:utf-8
#name:mod_config.py

"""
    mod_config
    --------------

    获取config配置
"""


import ConfigParser
import os
path = r'config.conf'



def getConfig(section, key):
    """ 查找option
    """
    config = ConfigParser.ConfigParser()
    config.read(path)
    return config.get(section, key)

#其中 os.path.split(os.path.realpath(__file__))[0] 得到的是当前文件模块的目录

def setConfig(section,key,value):
    """ 设置option
    """
    config = ConfigParser.ConfigParser()
    config.readfp(open(path,'r'))

    if not config.has_section(section):
        config.add_section(section)

    config.set(section,key,value)
    config.write(open(path,"w"))

def hassection(section):
    """判断节点是否存在
    """
    config = ConfigParser.ConfigParser()
    config.read(path)
    return config.has_section(section)

def hasoption(section,option):
    """ 判断option是否存在
    """
    config = ConfigParser.ConfigParser()
    config.read(path)
    return config.has_option(section,option)

if __name__ == '__main__':
    setConfig('wsh','name','ww')
