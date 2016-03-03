# coding=utf-8

import os,sys
import re



#dir1 = r'/home/huihui/work/server/nodeserver/commands/libbase'
#dir1 = r'/data/release/yunwei/server/configserver'
#dir2 = os.getcwd()
#os.chdir(dir1)
#sys.path.append(dir1)
#from libbase.getConfigClient import  getres
#os.chdir(dir2)

from ...webclient.libbase.getConfigClient import getres

def sg_split(astr):
    """
    将接收的结果生成list
    """
    patt = re.compile('\(.*?\)')
    itemlist =  re.findall(patt,astr)
    sglist = []
    for item  in itemlist:
        alist=item.replace('(','').replace(')','').replace('\'','').replace(' ','').split(',')
        sglist += [alist,]
    return sglist

def getserverinfo():
    """
    获取所有的服务器信息，包括区游戏区号，value，ip(webip)，webname，dbcip，dbcname，
    dbip,dbname
    因为会存在 如果ip为 12的话 123 和 12 都会替换ip，所以代码加长了好多
    """
    sql = "selectbysql select  min(dbnum),max(dbnum),ip,dbc,db from domain group by ip,db,dbc"
    ipstrlist  = eval(getres(sql))


    
    
    sql= "selectbysql select name,ip from server"
    res = getres(sql)
    namelist = sg_split(res)

    #    有兴趣可以改下这个代码 #
    ipstr = '['
    for line  in  ipstrlist :
        linetmp  = list(line[:2])
        linetmp += [ str(item[0])+','+str(item[1]) for item in namelist for i in  line if i== item[1] ]

        ipstr +=  str(tuple(linetmp))
        #ipstr = ipstr.replace(str(item[1]),str(item[0])+','+str(item[1]))
    ipstr += ']'


    return sorted(sg_split(ipstr),key = lambda x : int(x[0]))

def getdbnuminfo():
    """ 获取游戏区号和value的对应关系"""
    sql = "selectbysql select  distinct dbnum,value from domain  where iswork=1 "
    res = getres(sql)
    dbnumlist = sg_split(res)
    print dbnumlist


    return  sorted(dbnumlist,key = lambda x : int(x[0]))

def dbnuminfo_one(dbnum):
    """获取一个区的详细信息,包含server，因为和serverinfo差不多，所以不做这个东西了"""
    pass


if __name__ == "__main__":
    print serverinfo()
