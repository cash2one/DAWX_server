#!/bin/env python
#coding=utf-8

# CSsqlite的再次封装
# Author： wsh
# Time : 2015-05-27


import CSsqlite

conn = ''

def init():
    global conn
    CSsqlite.init()
    conn = CSsqlite.getConn()
    return conn

def close():
    global conn
    conn.close()

def add(alist):
    """
    Arguments:
    - `tablename`:
    - `handledata`:
    """
    listitems = []
    for i in alist[0].split('|'):
        alist = i.split(',')
        if len(alist) != 5:
            return False
        alist[2] = int(alist[2])
        alist[3] = int(alist[3])
        listitems.append(tuple(alist))


    conn = init()
    sql = 'INSERT INTO domain values(?,?,?,?,?)'
    res = CSsqlite.save(conn,sql,listitems)
    close()
    return res


def update(alist):
    """
    Arguments:
    - `tablename`:
    - `handledata`:
    """
    # 重点部分，list处理，还有一点就是处理麻烦
    adict = {}
    for line in alist:
        name,value = line.split('=')
        adict[name] = value

    if 'dbnum' not in adict.keys():
        return [False, "You should add dbnum!"]
    if len(adict) != 2 :
        return [False,"You should input 2 argv"]

    if 'value' in adict.keys() :
        sql = 'UPDATE domain  SET value = ? WHERE dbnum = ? '
        handledata = [(adict['value'],adict['dbnum'])]
    elif 'iswork' in adict.keys():
        sql = 'UPDATE domain  SET iswork = ? WHERE dbnum = ? '
        handledata = [(adict['iswork'],adict['dbnum'])]
    elif 'ip' in adict.keys():
        sql = 'UPDATE domain  SET ip = ? WHERE dbnum = ? '
        handledata = [(adict['ip'], adict['dbnum'])]
    conn = init()
    res = CSsqlite.update(conn,sql,handledata)
    close()
    return res

def findbydb(alist):
    if len(alist) != 1:
        return [False , "You should input right command!!"]
    dbnum = int(alist[0])
    sql = '''select server.name,server.ip,domain.value,domain.domainname,domain.iswork from domain,server where domain.ip = server.ip and server.servertype like '%web%' and domain.dbnum =?'''

    conn = init()
    res = CSsqlite.fetchone(conn,sql,dbnum)
    close()
    return res

def findbyip(alist):
    if len(alist) != 1:
        return [False , "You should input right command!!"]
    ip = alist[0]
    sql = '''select server.name,server.ip,domain.dbnum,domain.value,domain.domainname,domain.iswork from domain,server where domain.ip = server.ip and domain.ip ='%s' ''' % ip

    conn = init()
    res = CSsqlite.fetchall(conn,sql)
    close()
    return res

def deletebydb(alist):
    """
    """
    if len(alist) != 1:
        return [False , "You should input right command!!"]
    dbnum = int(alist[0])

    sql = '''DELETE from domain WHERE dbnum = ?'''
    conn = init()
    res = CSsqlite.delete(conn,sql, dbnum)
    close()
    return res

def selectbysql(alist):
    """
    """
    sql = " ".join(alist)

    conn = init()
    res = CSsqlite.fetchall(conn,sql)
    close()
    return res


if __name__ == '__main__':
    selectcommand()

