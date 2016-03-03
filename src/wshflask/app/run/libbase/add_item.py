#coding=utf-8
"""
Looks up a host based on its name, and then adds an item to it
"""

from pyzabbix import ZabbixAPI, ZabbixAPIException
import sys
import time
import json
from ... import globalconfig


class DawxZabbix():
    def __init__(self):
        self.zapi = ZabbixAPI(globalconfig.ZABBIX_SERVER)
        self.zapi.login(globalconfig.ZABBIX_ADMIN, globalconfig.ZABBIX_PASSWORD)

    def gethostgroup(self):
        grouplist = self.zapi.hostgroup.get(output=["hostid","name"])
        name= []

        for group in grouplist:
            name.append((group[u'name'],group[u'groupid']))
        return  name

    def gethost(self,hostsgroupid,**kwargs):
        hostlist =  self.zapi.host.get(output=["host","name"],groupids=hostsgroupid,**kwargs)
        return [ (host[u'name'],host[u'hostid'])  for host in hostlist ]

    def getitem(self,hostid,**kwargs):
        """
          因为item中有一些name属性含有$1,$2这种符号，所以需要替换为key_属性的第一个或者第二个。
        """
        import re

        itemlist = self.zapi.item.get(output=["name","key_"], hostids= hostid, **kwargs)
        newlist = []
        for item in itemlist:
            if int(item[u'itemid']) == 27337:
                print item
            if '$1' in item[u'name']: 
                newstr = re.search('\[.*?\]',item[u'key_']).group(0)[1:-1].split(',')[0]
                item[u'name'] = item[u'name'].replace(u'$1',newstr)
            if '$2' in item[u'name']:
                newstr = re.search('\[.*?\]',item[u'key_']).group(0)[1:-1].split(',')[1]
                item[u'name'] = item[u'name'].replace(u'$2',newstr)

            newlist.append((item[u'name'],item[u'itemid']))

        return newlist

    def getapplication(self,hostid,**kwargs):
        applicationlist = self.zapi.application.get(output="extend",hostids=hostid,**kwargs)
        return [ (application[u'name'],application[u'applicationid'],) for application in applicationlist ] 

    def getcommonhosts(self):
        grouplist = self.gethostgroup()
        alist = []
        for group in grouplist:
            groupid = group[1]
            groupname = group[0]
            hostlist =  self.gethost(groupid)
            alist.append((groupid,groupname,hostlist))
        return  json.dumps(alist)
        """
        for i in astr:
            print [x[0] for x in i[2] ]
        """

    def gethistory(self,itemidlist,**kwargs):
        historylist = self.zapi.history.get(output="extend",history="3",itemids=itemidlist, **kwargs)
        data_timeline = [x[u'clock'] for x in historylist ]
        value_line = [x[u'value'] for x in historylist]
        return data_timeline,value_line

    def historysum(self,itemidlist,**kwargs):
        # 没有考虑时间超过的情况
        historylist = self.zapi.history.get(output="extend",history="3",itemids= itemidlist,limit=len(itemidlist),sortfield="clock", **kwargs)
        sum = 0
        # alist 用来临时存储itemidlist
        alist = []
        for history in historylist:
            print history
            if history[u'itemid'] in alist :
                continue
            alist.append(history[u'itemid'])
            print sum
            sum = sum + int(history[u'value'])
        return sum


    def wshtest(self, itemidlist):
        historylist = self.zapi.history.get(output="extend",history="3",itemids= itemidlist,limit="100")
        print historylist
        data_timeline = [x[u'clock'] for x in historylist ]
        value_line = [x[u'value'] for x in historylist]
        print data_timeline

        return data_timeline,value_line

if __name__ == '__main__':
    ainstance = DawxZabbix()
    #    print ainstance.wshtest()
    print ainstance.getapplication('10108')

    """
            applicationlist =  ainstance.getapplication(hostid)
            for application in applicationlist:
                applicationid = application[u'applicationid']
                itemlist = ainstance.getitem(hostid,applicationid)
                for item in itemlist:
                    print item
    """
    
#
#template = zapi.template.create(host="dawx_test",groups={"groupid":1})
# template = zapi.hostgroup.create(name="dawx")
#template = zapi.hostgroup.create(name="dawx123")
#template = zapi.hostgroup.delete("15","16")
#template = zapi.template.get(output=["host","name","description"])

"""
        item=zapi.item.create(
            hostid=host_id,
            name='Used disk space on $1 in %',
            key_='vfs.fs.size[/,pused]',
            type=0,
            value_type=3,
            interfaceid=hosts[0]["interfaces"][0]["interfaceid"],
            delay=30
        )
"""
