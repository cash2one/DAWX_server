#!/bin/bash

.  /etc/profile


echo "You input : " $@

if [[ $# != 5 ]];
then
	  echo "shell ARGV number ERROR!!!"
	  exit 100
fi

tag=$1
ip=$2
start=$3
end=$4
numeval=$5

if [ $tag == "bind"  ];then
    cmd="qc-domain-bind"
elif [ $tag == "unbind" ];then
    cmd="qc-domain-unbind"
else
    echo "tag error"
    exit 100
fi
echo "start " + ${start}
echo "end " + ${end}
echo "numeval" + ${numeval}

for i  in `seq  ${start} ${numeval} ${end} `
do
    ${cmd} --domain=s${i}.app1101376335.qqopenapp.com --ips=${ip} --ports=80
done


