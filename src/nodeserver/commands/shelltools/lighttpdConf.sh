#!/bin/bash
# Author : hui
# date : 20150701
# content: lighttpd的更改
# Note ：

dir1='/usr/local/services/lighttpd/sbin/'

ip=$1
echo "LighttpdConf.sh  start..............."
echo "ip = "${ip}
date1=`date +%Y%m%d`
# 1, 移除httpd配置
yes | mv ${dir1}/host.conf ${dir1}/host.conf${date1}


astr=`python commands/libbase/getConfigClient.py findbyip ${ip}`
echo "------"
echo $astr


echo "" >  ${dir1}/host.conf
ass=`echo ${astr//\),/\)} |tr -d "[](' " |tr "\)" " "`
echo "ass = "$ass
for i in $ass
do
	dbnum=`echo $i |awk -F"," '{print $3}'`
	dbname=`echo $i |awk -F"," '{print $5}'`
	echo "\$HTTP[\"host\"] == \""${dbname}"\"{"  >> ${dir1}/host.conf
	echo "    server.document-root = \"/data/release/sgonline/s"${dbnum}"/webroot/\"" >> ${dir1}/host.conf
	echo "}" >> ${dir1}/host.conf
done





