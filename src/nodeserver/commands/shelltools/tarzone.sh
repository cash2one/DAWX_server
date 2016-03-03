#!/bin/bash

# tar gamezone in two parts,one has  data and today log, another has other log
# Author: wsh
# Time: 2015-05-25
# 
time1=`date +%Y%m%d`

withlogtag=0
echo "Warning: you will tar  "$#"  gamezones"
echo "include: " $@


tardir1="/data/release/yunwei/tar/"
tempdir1="/data/release/yunwei/temp/"

echo "Now delete pre-tar.................."

rm -rf  ${tardir1}/*
echo "delete pre-tar OK!!!!!!!!!!!!!"

echo "Now tar..............................."
for i in $@
do
	echo $i
	cd /usr/local
	pwd
	tar   -rhf ${tardir1}gamezonemonitors${time1}log.tar monitor_sanguo_s${i} stat_s${i} script/sanguo_s${i}

	
	cd /data/release/sgonline
	if ! [ -d "s"$i ];
	then
        echo  "s"$i"  not exists, please check it"
        exit 100
	fi

	tar -rf ${tardir1}gamezone${time1}.tar --exclude=./s${i}/datalog --exclude=./s${i}/vedio  --exclude=./s${i}/log ./s${i}
	tar  -rf ${tardir1}gamezone${time1}.tar ./s${i}/log/business/*`date +%Y%m%d`*
	if [ $withlogtag -eq 1 ];
	then
		echo "tar log"
		tar  -rf ${tardir1}/gamezone${time1}log.tar --exclude=./s${i}/log/business/*`date +%Y%m%d`* ./s${i}/log
	else
		echo "not tar log"
	fi

	mv ./s${i}   ${tempdir1}/
	
done

echo "tar is  done........................."
echo "You should unrar these files whith -C "
#  tar -xvf  monitors20150525log.tar.gz  -C /data/release/yunwei






		 
