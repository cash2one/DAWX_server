#coding=utf-8
from datetime import datetime
from flask import render_template,session,redirect,url_for,request
import time

from . import api
from ...webclient import runcmd
from ..libbase.serverinfo import  sg_split


from ..libbase.add_item import DawxZabbix
import json

@api.route('/getitems')
def getitems():
    kwargs = request.args.to_dict()
    ainstance = DawxZabbix()
    if 'hostid' in kwargs.keys():
        hostidlist = kwargs['hostid']
        del(kwargs['hostid'])
        print hostidlist
        res = ainstance.getitem(hostidlist,**kwargs)
        return json.dumps(res)
    return 'None'


@api.route('/gethostgroups')
def gethostgroups():
    # 这个id无用
    hostgroupid =request.args.get('id')
    ainstance = DawxZabbix()
    return json.dumps(ainstance.gethostgroup())


@api.route('/gethosts')
def gethosts():
    hostgroupid =request.args.get('id')
    ainstance = DawxZabbix()
    return json.dumps(ainstance.gethost(hostgroupid))

@api.route('/getapplications')
def getapplications():
    hostid = request.args.get('hostid')
    ainstance = DawxZabbix()
    return json.dumps(ainstance.getapplication(hostid))


@api.route('/getiteminfo')
def getiteminfo():
    itemid =[request.args.get('id')]
    ainstance = DawxZabbix()
    res = ainstance.wshtest(itemid)
    print res
    adict = {u'timelist':res[0], u'datalist': res[1]}
    return json.dumps(adict)

#@api.route('/gethistory')
def gethistory(time_eval,days_eval,**kwargs):
    #kwargs = request.args.to_dict()
    ainstance = DawxZabbix()
    time_till = int(time.time()) - int(time_eval)*86400
    time_from = time_till - 86400*int(days_eval)
    if 'itemids' in kwargs.keys():
        itemidlist = kwargs['itemids']
        del(kwargs['itemids'])
        kwargs['time_from'] = time_from
        kwargs['time_till'] = time_till
        res = ainstance.gethistory(itemidlist,**kwargs)
        #adict = {u'timelist':res[0],u'datalist':res[1]}
        if (int(time_eval) == 0 ):
            time_eval = "today"
        elif (int(time_eval) == 1):
            time_eval = "Yesterday"
        else:
            time_eval = str(int(time_eval)+1) + " days ago"

        adict = {u'timelist':res[0], u'datalist':{'name':time_eval,'type':'line','data':res[1]},'lengend':time_eval}
        return adict
    return 'None'


@api.route('/getposthistory')
def getposthistory():
    kwargs = request.args.to_dict()
    alist = kwargs['time_eval'].split(',')
    days_eval = kwargs['days_eval']
    del kwargs['days_eval']
    del kwargs['time_eval']
    minval = min(alist)
    datalist ={u'timelist':[],u'datalist':[],u'lengend':[]}
    for i in alist:
        adict = gethistory(i,days_eval,**kwargs)
        if i == minval:
            datalist[u'timelist'] = adict[u'timelist']
        datalist[u'datalist'] += [adict[u'datalist'],]
        datalist[u'lengend']  += [adict[u'lengend'],]
    print datalist
    return json.dumps(datalist)








def gethistory_item(time_eval,days_eval,**kwargs):
    #kwargs = request.args.to_dict()
    ainstance = DawxZabbix()
    time_till = int(time.time()) - int(time_eval)*86400
    time_from = time_till - 86400*int(days_eval)
    lengend = kwargs['itemids']
    if 'itemids' in kwargs.keys():
        itemidlist = kwargs['itemids']
        del(kwargs['itemids'])
        kwargs['time_from'] = time_from
        kwargs['time_till'] = time_till
        res = ainstance.gethistory(itemidlist,**kwargs)
        #adict = {u'timelist':res[0],u'datalist':res[1]}
        if (int(time_eval) == 0 ):
            time_eval = "today"
        elif (int(time_eval) == 1):
            time_eval = "Yesterday"
        else:
            time_eval = str(int(time_eval)+1) + " days ago"

        adict = {u'timelist':res[0], u'datalist':{'name':lengend,'type':'line','data':res[1]},'lengend':lengend}
        print adict
        return adict
    return 'None'





@api.route('/getitemshistory')
def getitemshistory():
    kwargs = request.args.to_dict()
    alist = kwargs['itemids'].split(',')
    print "itemids list is " + str(alist)
    days_eval = kwargs['days_eval']
    time_eval = kwargs['time_eval']
    del kwargs['itemids']
    del kwargs['days_eval']
    del kwargs['time_eval']

    max = 0
    datalist ={u'timelist':[],u'datalist':[],u'lengend':[]}
    adictlist = []
    for i in alist:
        kwargs['itemids'] = i
        adict = gethistory_item(time_eval,days_eval,**kwargs)
        adict[u'len'] = len(adict[u'datalist'])
        max =max if max > adict[u'len'] else adict[u'len']
        adictlist.append(adict)

    for adict in adictlist:
        if max ==  adict[u'len']:
            datalist[u'timelist'] = adict[u'timelist']
        else:
            adict[u'datalist'] = [0]*(max - adict[u'len']) + adict[u'datalist']
        datalist[u'datalist'] += [adict[u'datalist'],]
        datalist[u'lengend']  += [adict[u'lengend'],]

    return json.dumps(datalist)

@api.route('/getdbnumbyvalue')
def getdbnumbyvalue():
    valueid =request.args.get('id')
    sql = "selectbysql select dbnum from domain where value= %d" % int(valueid)
    alist =[ item[0] for item in sg_split(runcmd(sql)) ]
    return json.dumps(alist)
