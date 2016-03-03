#!/bin/bash
# hequ
# Author: wsh
# time: 2015-05-25


alist=$*
targetzone=$1

echo $1
echo $targetzone

for i in $alist 
do
   astr1=$astr1\"s$i\"\,
   astr2=$astr2$i\,
   astr3=$astr3" "$i
done
astr1=`echo $astr1  |sed 's/,$//' `
astr2=`echo $astr2  |sed 's/,$//' `
astr4=`echo $astr3 |awk -F" " '{$1="";print}'`
echo $astr1
echo $astr2
echo $astr3
echo $astr4

filepath="/data/release/sgonline/s"$targetzone
filescripts=$filepath/scripts
filetools=$filepath/tools

echo "1.  change the file: clear_world.pl"
cp /data/release/sgonline/clear_world.pl  $filescripts/
#sed -i 's/\"s128\",\"s129\",\"s130\"/'"$astr1"'/g' $filescripts/clear_world.pl
sed -i 's/^\@clear_world\ =\ \(.*\);$/\@clear_world\ =\ \('${astr1}'\);/g' $filescripts/clear_world.pl

echo "2. change the file: ranklist_end.pl"
#sed -i 's/serverid_value/'"$astr2"'/g'   $filescripts/ranklist_end.pl 
sed -i 's/^\$servers\ =\ \"\(.*\)\";$/\$servers\ =\ \"\('${astr2}'\)\";/g'  $filescripts/ranklist_end.pl


cp /data/release/sgonline/Update*.sh $filetools/
echo "3. change the file : UpdateAllianceStat_merge.sh"
sed -i 's/^si=73;$/si='"$targetzone"';/g' $filetools/UpdateAllianceStat_merge.sh
sed -i 's/73\ 74\ 75/'"$astr3"'/g' $filetools/UpdateAllianceStat_merge.sh

echo "4. change the file: UpdateTimeLimitPayCount_merge.sh" 
sed -i 's/`seq 2 6`/'"$astr4"'/g'  $filetools/UpdateTimeLimitPayCount_merge.sh


echo "5. EXE  clear_world"
cd  $filescripts/
chmod +x ./clear_world.pl
./clear_world.pl  yes!
