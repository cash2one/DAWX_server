#!/bin/bash
#coding=utf-8

# 执行tarzone的前一步
# Author： wsh
# Time : 2015-06-23
# 目前有三个作用：
#     1. 在nodeserver 上面删除domai，之后执行tarzone.sh
#     2. 在合区的主服务器上面执行删除domai，之后进行合区
#     3. 在合区之后进行domai的添加。



echo "changeZoneConf.sh  start..............."
# 1. 更改domai
command=$1
if [ ${command} == "add" ];
then
	  tag="--add"
elif [ ${command} == "delete" ];
then
    tag="--delete"
else
    exit 100
fi 

shift
dbnumlist=$@

for dbnum in ${dbnumlist}
do
	# 对于domai_conf进行更改
	python commands/libbase/domai_config.py ${tag} -d ${dbnum}
	if  ! [ $? -eq 0 ];
	then
		exit -1
	fi

done


#ip=`LC_ALL=C ifconfig  eth1 | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`

# 对于Lighttpd进行更改
#sh  commands/shelltools/lighttpdConf.sh ${ip}
#if  ! [ $? -eq 0 ];
#then
#	exit -1
#fi

# kill cgi
echo "kill cgi............."
ps aux|grep Cgi|grep cgi|grep sgonline|awk '{printf("kill -12 %s\n", $2);}'|bash

echo "changeZoneConf.sh  end..............."
