#!/bin/env python
#coding=utf-8


#  利用字典形式来处理函数判断
#  Author : wsh
#  Time: 2015-06-01

import   CSsqliteconsole

def usage():
    """
    """
    return  [True,"""##########################################
            these commands below are supported!"""]
    """
    print "---findbydb 218 "
    print "---update  dbnum=218 iswork=1"
    print "---delete 218"
    print "---add 192.168.100.1,3.xxt.cn,218,218,0(|192.168.100.1,3.xxt.cn,218,218,0)"
    print "---help"
    print "##########################################"
    """
    
def dataanalyse(data):
    dictname = {'findbydb':CSsqliteconsole.findbydb,
                'findbyip':CSsqliteconsole.findbyip,
                'update':CSsqliteconsole.update,
                'delete':CSsqliteconsole.deletebydb,
                'add': CSsqliteconsole.add,
                'selectbysql':CSsqliteconsole.selectbysql
                }
    alist = data.split()
    if not alist:
        return [False, "You should use the right command"]
    elif  alist[0] != 'help' and len(alist) < 2 :
        return [False, "command error, You should input right command!! "]
    handlecmd = alist[0]

    print alist[1:]
    if handlecmd in dictname.keys():
        return dictname[handlecmd](alist[1:])
    elif  handlecmd == 'help' :
        return usage()
    else:
        return [False , "You should use the right command"]

if __name__ == '__main__':
    dataanalyse('helpsd')
