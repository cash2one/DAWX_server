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

def getdbnuminfo():
    sql = "selectbysql select  distinct dbnum,value from domain  where iswork=1 "
    res = getres(sql)

    patt = re.compile('\(.*?\)')
    itemlist =  re.findall(patt,res)

    dbnumvaluelist={}
    for item  in itemlist:
        alist=item.split(',')

        if len(alist) < 2: break
        dbnum=0 if not alist[0] else int(filter(lambda x : x.isdigit(),alist[0]))
        value=0 if not alist[1] else int(filter(lambda x : x.isdigit(),alist[1]))
        if dbnum == 0 or value == 0: break
        if value in dbnumvaluelist.keys():
            dbnumvaluelist[value] += [dbnum,]
        else:
            dbnumvaluelist[value] = [dbnum,]

    return [(k,dbnumvaluelist[k]) for k in sorted(dbnumvaluelist.keys())]


if __name__ == "__main__":
    print dbnuminfo()
