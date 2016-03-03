#/bin/bash
#
# author :wsh
# time: 2015-06-17
# scp无非是从那个ip的目录的文件下载到那个目录下

. /data/release/yunwei/server/nodeserver/shellinit.conf


ip=$1
user=${DAWXUSER}
password=${DAWXPASSWD}
date1=`date "+%Y%m%d"`
dir1='/data/release/yunwei/tar/'
name=

# 清空该目录下的所有文件
rm -rf ${dir1}/*

/usr/bin/expect << EOF |tee 1.txt
set timeout 600

spawn scp $user@$ip:${dir1}/${name}*${date1}* ${dir1}
expect {
	"yes/no" {send "yes\r" ; exp_continue}
	"Password: "  {send "$password\r"}
    "password:" {send "$password\r"}
}
expect  {
	"file" {puts "EXECUTE ERROR"}
	eof {puts "EXECUTE OK"}
	}

EOF

geterr=`grep "EXECUTE ERROR" 1.txt`
getok=`grep "EXECUTE OK"  1.txt`

rm -rf  1.txt

if [[ -z "$getok" && ! -z "$geterr" ]];
then
	exit 100

fi

if [[ ! -z "$getok" && -z "$geterr" ]];
then
	cd ${dir1}
	tar xvf gamezone${date1}.tar -C /data/release/sgonline/
	tar xvf gamezonemonitors${date1}log.tar -C /usr/local/
fi


echo " scp.sh Execution"

