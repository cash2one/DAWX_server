#!/bin/bash
#coding=utf-8

# 执行tarzone的前一步
# Author： wsh
# Time : 2015-06-24
# 生成日志目录

dir1='/data/release/sgonline/'
dbnumlist=$@


cd $dir1

for dbnum in ${dbnumlist}
do
	mkdir -p  s${dbnum}/log/business/
	mkdir -p  s${dbnum}/vedio
    mkdir -p  s${dbnum}/datalog
done

