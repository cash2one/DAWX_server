#encoding:utf-8
#name:check.py

# date: 20150923
# author: wsh

"""
    Check
    --------------

    服务器启动之前检查一下是否符合启动条件，只需要改写或调用 **check()** ,如果无特殊需要就不用调用其他函数。
    分为一下几个方面::

        1. 文件夹是否存在
        2. 文件是否存在
        3. config参数是否存在


"""
import os,sys
from  mod_config import hasoption,getConfig

def checkdir(dir):
    """目录是否存在,是否有权限

    """
    if os.path.isdir(dir) and os.access(dir,os.W_OK):
        #print "dir check OK :: " + dir 
        return True
    elif not  os.path.isdir(dir):
        try:
            os.makedirs(dir)
        except Exception:
            print "dir check failed ,can't create dir::" + dir 
            return False
        return True
    else:
        print "dir check failed :: " + dir 
        return False



def checkfile(file):
    """文件是否存在，是否有权限
    """
    if os.path.isfile(file) and os.access(file,os.W_OK):
        #print "file check OK :: " + file 
        return True
    elif not  os.path.isfile(file):
        try:
            f = open(file, 'w')
            f.close()
        except Exception:
            print "file check failed , can't create file :: " + file
            return False

        return True
    else:
        print "file check failed :: " + file
        return False


def checkconfig(section,optionlist):
    """在 config.conf 中是否存在section以及optionlist
    """
    tag = True
    for option in optionlist:
        if not  hasoption(section,option):
            #print "config check OK :: " + str((section,option)) 
            print "config check failed :: " + str((section,option)) + "you must repair it!!!" 
            tag = False

    return True if tag else False


def check():
    """检查脚本，也是需要自定义的地方，以后需要动态生成。
    """
    dirlist = eval(getConfig('check','dirlist'))
    filelist = eval(getConfig('check','filelist'))
    conflist = eval(getConfig('check','conflist'))
    tag = True
    print "check dir staring ......................."
    for item in dirlist:
        if not  checkdir(item):
            tag = False
    print "check file starting ......................"
    for item in filelist:
        if not checkfile(item):
            tag = False
    print "check conf starting .........................."
    for item in conflist:
        if not checkconfig(item[0],item[1]):
            tag = False
    print "all check done........................."
    return tag



if __name__ == "__main__":
    main()
