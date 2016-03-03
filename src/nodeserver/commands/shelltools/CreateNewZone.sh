#!/bin/bash
# Author : hui
# date : 20150511 20150609
# content: create new zone
# Note ： templat 需要注意，软件不一样，这个也不一样

echo "You input : " $@

if [[ $# != 2 ]];
then
	echo "shell ARGV number ERROR!!!"
	exit 100
fi

zonename="s"$1
time=$2

dir1="/data/release/sgonline"
templat="$dir1"/newservertemplat
newzonedir="$dir1"/"$zonename"
# 获取程序目前的目录
dir2=`pwd`


# 20150528 add by wsh
if [ -d $newzonedir ];
then
	echo  $newzonedir"    exists, please check it"
	exit 100
fi

# 1. cp game zone data
cp $templat $newzonedir -rp

# 2. create a timestamp for the reward
if [ ! -n  "$time" ];
then
    echo "Time error ###########################################"
    read -p "please input the reward time for creating a timestamp : " time
fi


timeid=`date -d"$time" +%s`
echo $timeid

# install the game zone

cd "$newzonedir"
echo  "$timeid"  "${zonename:1}"
./open_new_server.sh "$timeid"  "${zonename:1}"

sleep 10

# update domai_config.xmil
# 当前shell脚本目录位置
cd $dir2

# 执行这个语句，然后判断是否正确执行
python commands/libbase/domai_config.py --add -d "${zonename:1}"
if  ! [ $? -eq 0 ];
then
	exit -1
fi

# checkcgi
cd $dir1/pi/cgi/
./CgiLogin

tag1=`./CgiLogin |grep  "REFUSED"`
echo $tag1
if [ ! -n "$tag1" ]; 
then 
    echo "Cgi error, Please check it" 
    ./CgiLogin
    exit -1
fi

# restart cgi
ps aux|grep Cgi|grep cgi|grep sgonline|awk '{printf("kill -12 %s\n", $2);}'|bash

# update lighttpd
 



    


