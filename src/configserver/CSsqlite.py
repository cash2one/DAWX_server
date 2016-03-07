#!/bin/env python
#coding=utf-8

# some API about sqlite
# Author : wsh
# Time: 2015-5-26
# Version: v0.1
# reference url: http://www.cnblogs.com/hongten/p/hongten_python_sqlite3.html#3192737

import sys
sys.path.append('libbase')

import sqlite3
import os

# libbase
from CSLogging import write_logger
from mod_config import getConfig

# global var

dbFilePath = getConfig('csserver','sqlitepath')
tableName = ''

def getConn():
    """连接sqlite
    
    """
    global dbFilePath
    conn = sqlite3.connect(dbFilePath)
    return conn

def getCursor(conn):
    """获取游标    
    """
    return conn.cursor()


def dropTable(conn,table):
    """如果表存在，就删除表，如果表中存在数据，使用该方法的要注意
    """
    if table is not None and table != '':
        sql = 'DROP TABLE IF EXISTS' + TABLE
        write_logger('debug','EXEC SQL: %s \n\t\t AND ARGV: %s' % (sql,TABLE))
        cu = getCursor(conn)
        cu.execute(sql)
        conn.commit()
        write_logger('INFO','DELETE TABLE %s SUCESS' % TABLE )
        closeAll(conn,cu)
    else:
        
        print('the [{0}] is empty or equal None'.format(sql))


def createTable(conn,sql):
    """ 创建数据库
    """
    if sql.split() :
        cu = getCursor(conn)
        write_logger('debug','EXEC SQL: %s' % sql)
        cu.execute(sql)
        conn.commit()
        write_logger('INFO','EXEC SQL: %s' % sql)
        closeAll(conn,cu)
    else:
        print("The [{0}] is empty or equal None !".format(sql))

    
def closeAll(conn,cu):
    """关闭连接
    """
    try :
        if cu is not None:
            cu.close()

    finally:
        if cu is not None:
            cu.close()

def save(conn, sql, data):
    """保存数据
    """
    if sql.split():
        if data is not None:
            cu = getCursor(conn)
            for d in data:
                write_logger('debug','EXEC SQL: %s  ' % sql)
                cu.execute(sql, d)
                conn.commit()
            closeAll(conn,cu)
        return [True,data]
    else:
        print('the [{0}] is emptry or equal None!'.format(sql))
        return [False, "SQL error"]

def fetchall(conn,sql):
    """查找，并返回所有的结果
    """
    if sql.split():
        cu = getCursor(conn)

        cu.execute(sql)
        r = cu.fetchall()
        res = []
        if len(r) > 0:
            for atuple in r :
                j = ()
                for i in atuple:
                    j += (str(i),)
                res.append(j)

        return [True,res]
    
    else:
        print('the [{0}] is empty or equal None'.format(sql))


def fetchone(conn,sql,data):
    """查找，只返回一条结果
    """
    if sql.split():
        alist = []
        if data is not None:
            # Do this instead
            d = (data,)
            cu = getCursor(conn)
            write_logger('debug','EXEC SQL: %s \n\t\t AND ARGV: %s' % (sql,data))
            cu.execute(sql,d)
            r = cu.fetchall()
            res = []
            if len(r) > 0:
                for atuple in r :
                    j = ()
                    for i in atuple:
                        j += (str(i),)
                    res.append(j)
                        
                return [True,res]
        else:
            write_logger('ERROR','the command error!!')
    else:
        write_logger('ERROR','the sql is wrong!!')

    return [False,"sql error"]

    


def update(conn,sql,data):
    """更新数据
    """
    if sql.split():
        if data is not None:
            cu = getCursor(conn)
            for d in data:
                cu.execute(sql,d)
                conn.commit()

            closeAll(conn,cu)
            return [True,"UPDATE SUCESS"]
    else:
        write_logger('error','%s is empty or equal None' % sql)
        return [False,"UPDATE error"]

def delete(conn,sql,data):
    if sql.split():
        if data is not None:
            cu = getCursor(conn)
            d = (data,)
            write_logger('DEBUG','EXEC SQL: %s' % sql)
            cu.execute(sql,d)
            conn.commit()
            closeAll(conn,cu)
            return [True,"DELETE OK"]
    else:
        write_logger('error','%s is empty or equal None' % sql)
        return [False,"DELETE SQL ERROR"]

def init():
    """初始化全局数据库目录
    """
    global dbFilePath
    


if __name__ == '__main__':
    init()
    create_sql1='''CREATE TABLE 'server'(
    'name' TEXT not null,
    'ip'   TEXT not null,
    servertype TEXT not null
    )'''
    create_sql2='''CREATE TABLE 'domain'(
    'ip'   TEXT not null,
    'domainname' TEXT not null,
    'value'   int  not null,
    'dbnum'   int  not null
    )'''
    conn = getConn()
    #createTable(conn,create_sql1)
    #createTable(conn,create_sql2)
    #save_sql = '''INSERT INTO domain values(?,?,?,?,?)'''
    #data = [('192.168.100.1', '3.xxt.cn', 218, 218, )]
    #save(conn,save_sql,data)
    #sql = 'SELECT * from domain where dbnum = ?'
    sql ='''select server.name,server.ip,domain.value,domain.domainname,domain.iswork from domain,server where domain.ip = server.ip and iswork =1 and domain.ip ='%s' '''
    data = '10.190.169.146'
    sql =sql % data
    print sql
    print fetchall(conn,sql)
    conn.close()
    
    


    
