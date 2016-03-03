#coding=utf-8
"""
Looks up a host based on its name, and then adds an item to it
"""

from pyzabbix import ZabbixAPI, ZabbixAPIException
import sys

# The hostname at which the Zabbix web interface is available
ZABBIX_SERVER = 'http://192.168.100.252:8001/zabbix/'

zapi = ZabbixAPI(ZABBIX_SERVER)

# Login to the Zabbix API
zapi.login('Admin', 'zabbix')
host_name = '192.168.100.240'

#hosts = zapi.host.get(filter={"host": host_name},selectInterfaces=["interfaceid"])
# 获取 name为 Linux servers的主机的所有列表
#grouplist = zapi.hostgroup.get(output=["hostid","name"], filter={"name":"Linux servers"})
# 获取 linuxservers（id=2）下面的 host为"192.168.100.245"的属性
#hostlist  = zapi.host.get(output=["host","status","snmp_available"],groupids="2",filter={"host":"192.168.100.245"})
# 192.168.100.245 hostid : 10109

#itemlist = zapi.item.get(output=["itemids","key_"], hostids=["10109"],filter={"key_":"cpu"})
#applicationlist = zapi.application.get(output="extend",hostids="10109")

#itemlist = zapi.item.get(output=["name","key_"], hostids=["10109"],filter={}, applicationids="566" )
#historylist = zapi.history.get(output="extend",history="3",itemids=["24670"],limit=3)


def wshtest():
    # The hostname at which the Zabbix web interface is available
    ZABBIX_SERVER = 'http://192.168.100.252:8001/zabbix/'
    
    zapi = ZabbixAPI(ZABBIX_SERVER)
    zapi.login('Admin', 'zabbix')
    host_name = '192.168.100.240'
    itemlist = zapi.item.get(output=["name","key_"], hostids=["10109"],filter={}, applicationids="566" )
    historylist = zapi.history.get(output="extend",history="3",itemids=["24670"],limit="100")
    data_timeline = ",".join([ x['clock'] for x in historylist ])
    value_line = ",".join([x['value'] for x in historylist])
    return data_timeline,value_line

print wshtest()
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
