#encoding:utf-8
#name:mod_config.py

import ConfigParser
import os

#获取config配置文件
def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    path = r'config.conf'
    config.read(path)
    return config.get(section, key)

#其中 os.path.split(os.path.realpath(__file__))[0] 得到的是当前文件模块的目录


if __name__ == '__main__':
    dbname = getConfig("domai", "filepath")
    print dbname
