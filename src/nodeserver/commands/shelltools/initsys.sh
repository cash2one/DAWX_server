#!/bin/bash
# Author : hui
# date : 20151013
# content: 初始化系统
# Note ：



scp app1101376335@10.221.164.175:/data/home/app1101376335/authorized_keys .
# 1. 配置root自动登录

sudo su


wget  http://10.190.166.254/wsh/authorized_keys . 

mkdir /root/.ssh
mv authorized_keys  /root/.ssh/
chmod  600 -R /root/.ssh
cd /tmp
scp  app1101376335@10.221.164.175:/tmp/installzabbixagent.sh .
